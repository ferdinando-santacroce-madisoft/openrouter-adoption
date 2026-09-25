#!/usr/bin/env python3
"""Drift detection fra le pagine Confluence e lo stato registrato nel manifest.

Confronta il numero di versione corrente di ogni pagina pubblicata con il
runtime field `confluence_version` del manifest di migrazione. Se la versione
Confluence è maggiore, qualcuno ha modificato la pagina dopo la nostra ultima
pubblicazione: il contenuto esterno va recepito (o scartato con decisione
esplicita) prima di qualsiasi nuovo update, altrimenti verrebbe sovrascritto.

Di default opera sul manifest della selezione software OpenRouter; con --manifest
può operare su altri manifest che seguono lo stesso schema.

Sottocomandi:
  check           verifica drift su tutte le pagine published (sola lettura)
  snapshot save   salva lo snapshot HTML pubblicato e aggiorna il manifest
  diff            diff testuale fra snapshot locale e pagina corrente

Uscite: 0 = nessun drift, 1 = drift rilevato, 2 = errore/manifest stantio.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_MANIFEST_PATH = REPO_ROOT / "manifest-confluence.yaml"
DEFAULT_SNAPSHOT_DIR = REPO_ROOT / "snapshots-confluence"
DEFAULT_MANIFEST_LABEL = "OpenRouter"

# Default: manifest della selezione software OpenRouter. Con --manifest (e
# opzionalmente --snapshot-dir/--label) si opera su altri manifest con lo
# stesso schema.
MANIFEST_PATH = DEFAULT_MANIFEST_PATH
SNAPSHOT_DIR = DEFAULT_SNAPSHOT_DIR
MANIFEST_LABEL = DEFAULT_MANIFEST_LABEL
ARTIFACT_ROOT = REPO_ROOT

TWG_TIMEOUT = 120

DISPOSITIONS_PUBLISHABLE = {"publish_page", "synthesize"}


@dataclass
class Target:
    """Un target Confluence risolto dal manifest."""

    source: str
    target_key: str
    title: str
    content_id: str
    publication_status: str | None
    confluence_version: int | None
    published_body_path: str | None
    published_body_sha256: str | None
    node: dict  # dict ruamel dell'artifact o del target annidato

    @property
    def snapshot_path(self) -> Path:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "__", self.target_key)
        return SNAPSHOT_DIR / f"{safe}.html"


class Manifest:
    def __init__(self) -> None:
        yaml = YAML(typ="rt")
        yaml.preserve_quotes = True
        yaml.width = 4096
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.representer.add_representer(
            type(None), lambda dumper, _value: dumper.represent_scalar("tag:yaml.org,2002:null", "null")
        )
        self.yaml = yaml
        self.data = yaml.load(MANIFEST_PATH.read_text(encoding="utf-8"))

    def save(self) -> None:
        import io

        buf = io.StringIO()
        self.yaml.dump(self.data, buf)
        MANIFEST_PATH.write_text(buf.getvalue(), encoding="utf-8")

    def hierarchy_content_id(self, key: str) -> str | None:
        entry = (self.data.get("target_hierarchy") or {}).get(key) or {}
        cid = entry.get("content_id")
        return str(cid) if cid else None

    def targets(self, published_only: bool = True) -> list[Target]:
        out: list[Target] = []
        for art in self.data.get("artifacts") or []:
            if art.get("disposition") not in DISPOSITIONS_PUBLISHABLE:
                continue
            if art.get("targets"):
                for sub in art["targets"]:
                    t = self._make_target(art, sub)
                    if t and t.content_id:
                        out.append(t)
            else:
                t = self._make_target(art, art)
                if t and t.content_id:
                    out.append(t)
        if published_only:
            out = [t for t in out if (t.publication_status or "") == "published"]
        return out

    def _make_target(self, art: dict, node: dict) -> Target | None:
        cid = node.get("content_id") or art.get("content_id")
        if not cid:
            key = node.get("target_key") or art.get("target_key")
            cid = self.hierarchy_content_id(key) if key else None
            if cid:
                # content_id risolto dalla gerarchia (es. homepage): registrato
                # nel nodo solo se il nodo è l'artifact stesso.
                if node is not art:
                    cid = None
        if not cid:
            return None
        return Target(
            source=str(art.get("source")),
            target_key=str(node.get("target_key") or art.get("target_key") or art.get("source")),
            title=str(node.get("title") or art.get("title") or art.get("source")),
            content_id=str(cid),
            publication_status=node.get("publication_status") or art.get("publication_status"),
            confluence_version=_to_int(node.get("confluence_version") or art.get("confluence_version")),
            published_body_path=node.get("published_body_path") or art.get("published_body_path"),
            published_body_sha256=node.get("published_body_sha256") or art.get("published_body_sha256"),
            node=node,
        )


def _to_int(value: object) -> int | None:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def twg(args: list[str]) -> Path:
    """Esegue un comando twg con output JSON su file e restituisce il path."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        out = Path(tmp.name)
    cmd = ["twg", *args, "--output", "json", "--output-file", str(out)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TWG_TIMEOUT)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"twg timeout: {' '.join(cmd)}") from exc
    if proc.returncode != 0:
        raise RuntimeError(f"twg fallito ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr.strip()[:500]}")
    return out


def get_page_metadata(content_id: str) -> dict:
    path = twg(["confluence", "content", "get", content_id, "--include-metadata", "--agent-fields", "@metadata"])
    data = json.loads(path.read_text(encoding="utf-8")).get("data", {})
    path.unlink(missing_ok=True)
    return data


def get_page_body(content_id: str, dest: Path) -> None:
    path = twg(["confluence", "content", "get", content_id, "--detail", "full", "--format", "html", "--body-only"])
    dest.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    path.unlink(missing_ok=True)


def list_versions(content_id: str, limit: int = 20) -> list[dict]:
    path = twg(["confluence", "content", "versions", "list", "--id", content_id, "--limit", str(limit)])
    data = json.loads(path.read_text(encoding="utf-8")).get("data", [])
    path.unlink(missing_ok=True)
    return data


def cmd_check(manifest: Manifest, only_target: str | None, as_json: bool) -> int:
    targets = manifest.targets(published_only=True)
    if only_target:
        targets = [t for t in targets if t.target_key == only_target]
        if not targets:
            print(f"Target non trovato o non published: {only_target}", file=sys.stderr)
            return 2

    results = []
    drift_count = 0
    error_count = 0
    for t in targets:
        entry: dict = {"target_key": t.target_key, "content_id": t.content_id, "title": t.title}
        try:
            meta = get_page_metadata(t.content_id)
            current = (meta.get("metadata") or {}).get("version", {}).get("number")
        except RuntimeError as exc:
            entry.update(status="error", detail=str(exc))
            error_count += 1
            results.append(entry)
            continue
        entry["current_version"] = current
        entry["manifest_version"] = t.confluence_version
        # staleness vs git (informativo): il sorgente e' cambiato dall'ultima pubblicazione?
        src = ARTIFACT_ROOT / t.source
        expected_sha = t.node.get("source_sha256")
        if src.exists() and expected_sha:
            if hashlib.sha256(src.read_bytes()).hexdigest() != expected_sha:
                entry["source_stale"] = True
        if current is None:
            entry.update(status="error", detail="versione non leggibile da twg")
            error_count += 1
        elif t.confluence_version is None:
            entry.update(status="manifest_stale", detail="confluence_version assente nel manifest")
            error_count += 1
        elif t.confluence_version is not None and current == t.confluence_version:
            entry.update(status="ok")
        elif t.confluence_version is not None and current < t.confluence_version:
            entry.update(status="manifest_stale", detail="versione nel manifest maggiore della corrente")
            error_count += 1
        else:
            manifest_version = t.confluence_version or 0
            external = [
                v for v in list_versions(t.content_id)
                if (vnum := _to_int(v.get("number"))) is not None and vnum > manifest_version
            ]
            entry.update(status="drift", external_versions=external)
            drift_count += 1
        results.append(entry)

    if as_json:
        print(json.dumps({"drift": drift_count, "errors": error_count, "results": results}, indent=2, ensure_ascii=False))
    else:
        print(f"Drift check {MANIFEST_LABEL}: {len(targets)} pagine published\n")
        for r in results:
            icon = {"ok": "🟢", "drift": "🔴", "manifest_stale": "⚠️ ", "error": "❌"}.get(r["status"], "❓")
            line = f"{icon} {r['target_key']} (id {r['content_id']})"
            if r["status"] == "ok":
                line += f": in sync (v{r['manifest_version']})"
            elif r["status"] == "drift":
                line += f": DRIFT, manifest v{r['manifest_version']} → corrente v{r['current_version']}"
                for v in r.get("external_versions", []):
                    line += f"\n    v{v.get('number')} {v.get('createdAt', '')[:10]} minor={v.get('minorEdit')} autore={v.get('authorId')} msg={v.get('message') or '(nessuno)'}"
            else:
                line += f": {r.get('detail')}"
            if r.get("source_stale"):
                line += "\n    ⚠️ sorgente git modificato dall'ultima pubblicazione (candidato a update, non e' drift esterno)"
            print(line)
        print(f"\nEsito: {drift_count} drift, {error_count} errori su {len(targets)} pagine.")
        if drift_count:
            print("HARD BLOCK: nessun update sulle pagine in drift prima della decisione di Nando (reintegro nel git, scarto esplicito o richiesta al collega).")
    if drift_count:
        return 1
    if error_count:
        return 2
    return 0


def _resolve_node(manifest: Manifest, t: Target) -> tuple[dict, dict]:
    """Restituisce (artifact, nodo) su cui scrivere i runtime fields."""
    art = t.node
    if isinstance(art.get("targets"), list):
        for sub in art["targets"]:
            if str(sub.get("target_key")) == t.target_key:
                return art, sub
    return art, art


def cmd_snapshot_save(manifest: Manifest, all_targets: bool, only_target: str | None, force: bool, publish: bool = False) -> int:
    targets = manifest.targets(published_only=not all_targets)
    if only_target:
        candidates = manifest.targets(published_only=False)
        targets = [t for t in candidates if t.target_key == only_target]
        if not targets:
            print(f"Target non trovato (o senza content_id): {only_target}", file=sys.stderr)
            return 2

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    today = None
    from datetime import date

    today = date.today().isoformat()
    failures = 0
    for t in targets:
        art, node = _resolve_node(manifest, t)
        try:
            meta = get_page_metadata(t.content_id)
            current = (meta.get("metadata") or {}).get("version", {}).get("number")
            get_page_body(t.content_id, t.snapshot_path)
        except RuntimeError as exc:
            print(f"❌ {t.target_key}: {exc}")
            failures += 1
            continue
        body = t.snapshot_path.read_bytes()
        sha = hashlib.sha256(body).hexdigest()
        rel = str(t.snapshot_path.relative_to(ARTIFACT_ROOT))
        node["published_body_path"] = rel
        node["published_body_sha256"] = sha
        node["last_drift_check_at"] = today
        drift_here = (
            t.confluence_version is not None and current is not None and current != t.confluence_version
        )
        if current is not None and (not drift_here or force or publish):
            # --force registra lo stato osservato come nuova baseline (dopo la
            # decisione di Nando sul drift); senza drift l'aggiornamento è neutro.
            # --publish registra una pubblicazione dal repository appena eseguita:
            # la nuova versione è nostra, non drift esterno.
            node["confluence_version"] = str(current)
        if publish and current is not None:
            node["last_published_at"] = today
            src = ARTIFACT_ROOT / t.source
            if src.exists():
                node["source_sha256"] = hashlib.sha256(src.read_bytes()).hexdigest()
        note = ""
        if drift_here and not publish:
            note = f" ⚠️ versione cambiata da v{t.confluence_version} a v{current} (drift registrato nello snapshot)"
            if not force:
                print(f"🔴 {t.target_key}: drift rilevato (v{t.confluence_version} → v{current}); snapshot salvato comunque, decisione di Nando richiesta prima di un update.")
        elif publish:
            note = " (registrazione pubblicazione dal repository: versione, data e sorgente aggiornati)"
        print(f"🟢 {t.target_key}: snapshot v{current} salvato ({rel}, sha256 {sha[:12]}…){note}")
    manifest.save()
    print(f"\nManifest aggiornato: {MANIFEST_PATH}")
    return 1 if failures else 0


class _HTMLToText(HTMLParser):
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "table", "thead", "tbody", "ul", "ol", "blockquote", "hr", "pre"}
    SKIP = {"script", "style"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.parts.append("\n\x00SKIP\x00")
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.parts.append("\x00ENDSKIP\x00\n")
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        raw = re.sub(r"\x00SKIP\x00.*?\x00ENDSKIP\x00", "", raw, flags=re.S)
        lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in raw.split("\n")]
        return "\n".join(ln for ln in lines if ln)


def html_to_text(html: str) -> str:
    parser = _HTMLToText()
    try:
        parser.feed(html)
        parser.close()
    except Exception:
        return html
    return parser.text()


def cmd_diff(manifest: Manifest, only_target: str) -> int:
    targets = [t for t in manifest.targets(published_only=False) if t.target_key == only_target]
    if not targets:
        print(f"Target non trovato (o senza content_id): {only_target}", file=sys.stderr)
        return 2
    t = targets[0]
    if not t.snapshot_path.exists():
        print(f"Snapshot mancante: {t.snapshot_path}. Esegui prima 'snapshot save'.", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory() as tmp:
        current = Path(tmp) / "current.html"
        get_page_body(t.content_id, current)
        old_text = html_to_text(t.snapshot_path.read_text(encoding="utf-8"))
        new_text = html_to_text(current.read_text(encoding="utf-8"))
    diff = list(difflib.unified_diff(
        old_text.splitlines(), new_text.splitlines(),
        fromfile=f"snapshot/{t.target_key} (v{t.confluence_version})",
        tofile=f"confluence/{t.target_key} (corrente)",
        lineterm="",
    ))
    if not diff:
        print(f"🟢 {t.target_key}: nessuna differenza fra snapshot e pagina corrente.")
        return 0
    print("\n".join(diff))
    return 1


def _apply_manifest_override(args: argparse.Namespace) -> None:
    """Applica --manifest/--snapshot-dir/--label prima di instanziare Manifest."""
    global MANIFEST_PATH, SNAPSHOT_DIR, MANIFEST_LABEL, ARTIFACT_ROOT
    if not args.manifest:
        return
    mp = Path(args.manifest).expanduser().resolve()
    MANIFEST_PATH = mp
    ARTIFACT_ROOT = mp.parent
    if args.snapshot_dir:
        SNAPSHOT_DIR = Path(args.snapshot_dir).expanduser().resolve()
    else:
        SNAPSHOT_DIR = ARTIFACT_ROOT / "snapshots-confluence"
    MANIFEST_LABEL = args.label or mp.parent.name


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", help="path del manifest YAML (default: manifest-confluence.yaml nella root del repo)")
    ap.add_argument("--snapshot-dir", help="directory degli snapshot HTML (default: sottocartella snapshots-confluence accanto al manifest)")
    ap.add_argument("--label", help="etichetta nei messaggi (default: OpenRouter, o nome della cartella del manifest)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="verifica drift sulle pagine published (sola lettura)")
    p_check.add_argument("--target", help="verifica un solo target_key")
    p_check.add_argument("--json", action="store_true", help="output JSON per consumo agentico")

    p_snap = sub.add_parser("snapshot", help="gestione snapshot HTML pubblicati")
    s_sub = p_snap.add_subparsers(dest="snap_cmd", required=True)
    p_save = s_sub.add_parser("save", help="salva lo snapshot corrente e aggiorna i runtime fields")
    p_save.add_argument("--target", help="un solo target_key")
    p_save.add_argument("--all", action="store_true", help="tutti i target con content_id (anche non published)")
    p_save.add_argument("--force", action="store_true", help="salva anche in presenza di drift, senza blocco")
    p_save.add_argument("--publish", action="store_true", help="registra una pubblicazione dal repository: aggiorna confluence_version, last_published_at e source_sha256 oltre allo snapshot")
    p_diff = sub.add_parser("diff", help="diff testuale fra snapshot locale e pagina corrente")
    p_diff.add_argument("--target", required=True, help="target_key da confrontare")

    args = ap.parse_args()
    _apply_manifest_override(args)
    manifest = Manifest()

    if args.cmd == "check":
        return cmd_check(manifest, args.target, args.json)
    if args.cmd == "snapshot":
        if args.target and args.all:
            ap.error("--target e --all sono mutualmente esclusivi")
        return cmd_snapshot_save(manifest, args.all, args.target, args.force, publish=getattr(args, "publish", False))
    if args.cmd == "diff":
        return cmd_diff(manifest, args.target)
    return 2


if __name__ == "__main__":
    sys.exit(main())
