#!/usr/bin/env python3
"""Drift detection fra i Google Docs e lo stato registrato nel manifest.

Confronta la versione corrente di ogni Google Doc pubblicato con il runtime
field `drive_version` del manifest. Se la versione Drive e' maggiore, qualcuno
ha modificato il documento dopo la nostra ultima pubblicazione: il contenuto
esterno va recepito (o scartato con decisione esplicita) prima di qualsiasi
nuovo push, altrimenti verrebbe sovrascritto.

Sottocomandi:
  check           verifica drift su tutti i documenti published (sola lettura)
  snapshot save   esporta il markdown pubblicato e aggiorna il manifest
  diff            diff testuale fra baseline locale e documento corrente

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
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_MANIFEST_PATH = REPO_ROOT / "manifest-gdrive.yaml"
DEFAULT_SNAPSHOT_DIR = REPO_ROOT / "snapshots-gdrive"
DEFAULT_MANIFEST_LABEL = "OpenRouter"

MANIFEST_PATH = DEFAULT_MANIFEST_PATH
SNAPSHOT_DIR = DEFAULT_SNAPSHOT_DIR
MANIFEST_LABEL = DEFAULT_MANIFEST_LABEL
ARTIFACT_ROOT = REPO_ROOT
ACCOUNT = "work"

GWS_TIMEOUT = 120

DISPOSITIONS_PUBLISHABLE = {"push", "publish_page"}


@dataclass
class Target:
    """Un target Google Drive risolto dal manifest."""

    source: str
    target_key: str
    title: str
    file_id: str
    publication_status: str | None
    drive_version: int | None
    modified_time: str | None
    baseline_path: str | None
    baseline_sha256: str | None
    node: dict

    @property
    def snapshot_path(self) -> Path:
        return SNAPSHOT_DIR / f"{self.target_key}.md"


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

    def targets(self, published_only: bool = True) -> list[Target]:
        out: list[Target] = []
        for art in self.data.get("artifacts") or []:
            if art.get("disposition") not in DISPOSITIONS_PUBLISHABLE:
                continue
            t = self._make_target(art)
            if t and t.file_id:
                out.append(t)
        if published_only:
            out = [t for t in out if (t.publication_status or "") == "published"]
        return out

    def _make_target(self, art: dict) -> Target | None:
        fid = art.get("file_id")
        if not fid:
            return None
        return Target(
            source=str(art.get("source")),
            target_key=str(art.get("target_key") or art.get("source")),
            title=str(art.get("title") or art.get("source")),
            file_id=str(fid),
            publication_status=art.get("publication_status"),
            drive_version=_to_int(art.get("drive_version")),
            modified_time=art.get("modified_time"),
            baseline_path=art.get("baseline_path"),
            baseline_sha256=art.get("baseline_sha256"),
            node=art,
        )


def _to_int(value: object) -> int | None:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def gws_json(args: list[str]) -> dict:
    """Esegue un comando gws-account e restituisce il JSON di stdout."""
    cmd = ["gws-account", ACCOUNT, *args]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=GWS_TIMEOUT)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"gws timeout: {' '.join(cmd)}") from exc
    if proc.returncode != 0:
        raise RuntimeError(f"gws fallito ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr.strip()[:500]}")
    out = proc.stdout
    start = out.find("{")
    if start < 0:
        raise RuntimeError(f"gws senza JSON in output: {' '.join(cmd)}")
    return json.loads(out[start:])


def get_file_metadata(file_id: str) -> dict:
    return gws_json([
        "drive", "files", "get",
        "--params", json.dumps({"fileId": file_id, "fields": "id,name,version,modifiedTime,mimeType"}),
    ])


def export_markdown(file_id: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "gws-account", ACCOUNT, "drive", "files", "export",
        "--params", json.dumps({"fileId": file_id, "mimeType": "text/markdown"}),
        "--output", dest.name,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=GWS_TIMEOUT, cwd=str(dest.parent))
    if proc.returncode != 0:
        raise RuntimeError(f"gws export fallito ({proc.returncode}): {proc.stderr.strip()[:500]}")


def normalize_md(text: str) -> str:
    """Normalizza il markdown esportato da Google Docs per il confronto testuale."""
    lines = []
    for ln in text.split("\n"):
        ln = ln.rstrip()
        # i titoli esportati da Docs sono in grassetto: "# **Titolo**" -> "# Titolo"
        ln = re.sub(r"^(#{1,6}\s+)\*\*(.+?)\*\*\s*$", r"\1\2", ln)
        lines.append(ln)
    return "\n".join(lines).strip() + "\n"


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
        entry: dict = {"target_key": t.target_key, "file_id": t.file_id, "title": t.title}
        try:
            meta = get_file_metadata(t.file_id)
            current = _to_int(meta.get("version"))
        except RuntimeError as exc:
            entry.update(status="error", detail=str(exc))
            error_count += 1
            results.append(entry)
            continue
        entry["current_version"] = current
        entry["manifest_version"] = t.drive_version
        current_mt = meta.get("modifiedTime")
        entry["current_modified_time"] = current_mt
        entry["manifest_modified_time"] = t.modified_time
        src = ARTIFACT_ROOT / t.source
        expected_sha = t.node.get("source_sha256")
        if src.exists() and expected_sha:
            if hashlib.sha256(src.read_bytes()).hexdigest() != expected_sha:
                entry["source_stale"] = True
        if not current_mt:
            entry.update(status="error", detail="modifiedTime non leggibile da gws")
            error_count += 1
        elif not t.modified_time:
            entry.update(status="manifest_stale", detail="modified_time assente nel manifest")
            error_count += 1
        elif current_mt == t.modified_time:
            entry.update(status="ok")
        elif current_mt < t.modified_time:
            entry.update(status="manifest_stale", detail="modified_time nel manifest piu' recente della corrente")
            error_count += 1
        else:
            entry.update(status="drift")
            drift_count += 1
        results.append(entry)

    if as_json:
        print(json.dumps({"drift": drift_count, "errors": error_count, "results": results}, indent=2, ensure_ascii=False))
    else:
        print(f"Drift check {MANIFEST_LABEL}: {len(targets)} documenti published\n")
        for r in results:
            icon = {"ok": "🟢", "drift": "🔴", "manifest_stale": "⚠️ ", "error": "❌"}.get(r["status"], "❓")
            line = f"{icon} {r['target_key']} (id {r['file_id']})"
            if r["status"] == "ok":
                line += f": in sync (v{r['manifest_version']})"
            elif r["status"] == "drift":
                line += f": DRIFT, modifica esterna rilevata (manifest {r.get('manifest_modified_time')} → corrente {r.get('current_modified_time')}, v{r['manifest_version']} → v{r['current_version']})"
            else:
                line += f": {r.get('detail')}"
            if r.get("source_stale"):
                line += "\n    ⚠️ sorgente git modificato dall'ultima pubblicazione (candidato a push, non e' drift esterno)"
            print(line)
        print(f"\nEsito: {drift_count} drift, {error_count} errori su {len(targets)} documenti.")
        if drift_count:
            print("HARD BLOCK: nessun push sui documenti in drift prima della decisione di Nando (reintegro nel git, scarto esplicito o richiesta al collega).")
    if drift_count:
        return 1
    if error_count:
        return 2
    return 0


def cmd_snapshot_save(manifest: Manifest, all_targets: bool, only_target: str | None, force: bool, publish: bool = False) -> int:
    targets = manifest.targets(published_only=not all_targets)
    if only_target:
        candidates = manifest.targets(published_only=False)
        targets = [t for t in candidates if t.target_key == only_target]
        if not targets:
            print(f"Target non trovato (o senza file_id): {only_target}", file=sys.stderr)
            return 2

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    from datetime import date

    today = date.today().isoformat()
    failures = 0
    for t in targets:
        node = t.node
        try:
            meta = get_file_metadata(t.file_id)
            current = _to_int(meta.get("version"))
            current_mt = meta.get("modifiedTime")
            export_markdown(t.file_id, t.snapshot_path)
        except RuntimeError as exc:
            print(f"❌ {t.target_key}: {exc}")
            failures += 1
            continue
        body = t.snapshot_path.read_bytes()
        sha = hashlib.sha256(body).hexdigest()
        rel = str(t.snapshot_path.relative_to(ARTIFACT_ROOT))
        node["baseline_path"] = rel
        node["baseline_sha256"] = sha
        node["last_drift_check_at"] = today
        drift_here = t.modified_time is not None and current_mt is not None and current_mt != t.modified_time
        if current is not None and (not drift_here or force or publish):
            node["drive_version"] = str(current)
        if current_mt is not None:
            node["modified_time"] = current_mt
        if publish and current is not None:
            node["last_published_at"] = today
            src = ARTIFACT_ROOT / t.source
            if src.exists():
                node["source_sha256"] = hashlib.sha256(src.read_bytes()).hexdigest()
        note = ""
        if drift_here and not publish:
            note = f" ⚠️ versione cambiata da v{t.drive_version} a v{current} (drift registrato nello snapshot)"
            if not force:
                print(f"🔴 {t.target_key}: drift rilevato (v{t.drive_version} → v{current}); baseline salvata comunque, decisione di Nando richiesta prima del push.")
        elif publish:
            note = " (registrazione push dal repository: versione, data e sorgente aggiornati)"
        print(f"🟢 {t.target_key}: baseline v{current} salvata ({rel}, sha256 {sha[:12]}…){note}")
    manifest.save()
    print(f"\nManifest aggiornato: {MANIFEST_PATH}")
    return 1 if failures else 0


def cmd_diff(manifest: Manifest, only_target: str) -> int:
    targets = [t for t in manifest.targets(published_only=False) if t.target_key == only_target]
    if not targets:
        print(f"Target non trovato (o senza file_id): {only_target}", file=sys.stderr)
        return 2
    t = targets[0]
    if not t.snapshot_path.exists():
        print(f"Baseline mancante: {t.snapshot_path}. Esegui prima 'snapshot save'.", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory() as tmp:
        current = Path(tmp) / "current.md"
        export_markdown(t.file_id, current)
        old_text = normalize_md(t.snapshot_path.read_text(encoding="utf-8"))
        new_text = normalize_md(current.read_text(encoding="utf-8"))
    diff = list(difflib.unified_diff(
        old_text.splitlines(), new_text.splitlines(),
        fromfile=f"baseline/{t.target_key} (v{t.drive_version})",
        tofile=f"gdrive/{t.target_key} (corrente)",
        lineterm="",
    ))
    if not diff:
        print(f"🟢 {t.target_key}: nessuna differenza fra baseline e documento corrente.")
        return 0
    print("\n".join(diff))
    return 1


def _apply_manifest_override(args: argparse.Namespace) -> None:
    global MANIFEST_PATH, SNAPSHOT_DIR, MANIFEST_LABEL, ARTIFACT_ROOT, ACCOUNT
    if not args.manifest:
        return
    mp = Path(args.manifest).expanduser().resolve()
    MANIFEST_PATH = mp
    ARTIFACT_ROOT = mp.parent
    if args.snapshot_dir:
        SNAPSHOT_DIR = Path(args.snapshot_dir).expanduser().resolve()
    else:
        SNAPSHOT_DIR = ARTIFACT_ROOT / "snapshots-gdrive"
    MANIFEST_LABEL = args.label or mp.parent.name
    if args.account:
        ACCOUNT = args.account


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", help="path del manifest YAML (default: manifest-gdrive.yaml nella root del repo)")
    ap.add_argument("--snapshot-dir", help="directory delle baseline markdown (default: snapshots-gdrive accanto al manifest)")
    ap.add_argument("--label", help="etichetta nei messaggi (default: OpenRouter, o nome della cartella del manifest)")
    ap.add_argument("--account", help="alias account gws (default: work)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="verifica drift sui documenti published (sola lettura)")
    p_check.add_argument("--target", help="verifica un solo target_key")
    p_check.add_argument("--json", action="store_true", help="output JSON per consumo agentico")

    p_snap = sub.add_parser("snapshot", help="gestione baseline markdown esportate")
    s_sub = p_snap.add_subparsers(dest="snap_cmd", required=True)
    p_save = s_sub.add_parser("save", help="esporta la baseline corrente e aggiorna i runtime fields")
    p_save.add_argument("--target", help="un solo target_key")
    p_save.add_argument("--all", action="store_true", help="tutti i target con file_id (anche non published)")
    p_save.add_argument("--force", action="store_true", help="salva anche in presenza di drift, senza blocco")
    p_save.add_argument("--publish", action="store_true", help="registra un push dal repository: aggiorna drive_version, last_published_at e source_sha256 oltre alla baseline")
    p_diff = sub.add_parser("diff", help="diff testuale fra baseline locale e documento corrente")
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
