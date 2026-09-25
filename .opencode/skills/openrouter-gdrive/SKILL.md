---
name: openrouter-gdrive
description: >-
  Sincronizzazione bidirezionale tra i documenti locali della selezione
  software OpenRouter (markdown in `contenuti/`) e i Google Docs della cartella
  Drive "Adozione OpenRouter" (account `work`), tramite la CLI `gws`. Gestisce
  il push locale -> Google Drive e la ricezione/modifica da Google Drive ->
  locale, con i check e le verifiche del caso (drift, baseline, read-back,
  commenti). Usa quando devi pubblicare un aggiornamento sui Google Docs della
  selezione software, recepire modifiche fatte direttamente sui Docs, o
  verificare lo stato di allineamento dei documenti OpenRouter.
---

# OpenRouter <-> Google Drive: sincronizzazione bidirezionale

## Contesto

- **Repo**: `openrouter-adoption` — i sorgenti markdown vivono in `contenuti/` (sorgente unica anche per il target Confluence).
- **Cartella Drive**: **Adozione OpenRouter** (`1bGRMC7V0k2kfulbsC-IUWVdOoYsVfUT1`), account `work` (`ferdinando.santacroce@madisoft.it`).
- **Control plane**: `manifest-gdrive.yaml` (artifacts, file_id, runtime fields).
- **Preparazione markdown**: `.opencode/skills/openrouter-gdrive/scripts/gen-md-gdrive.mjs`.
- **Drift check / baseline**: `.opencode/skills/openrouter-gdrive/scripts/verifica-drift-gdrive.py`.
- **Scrittura Drive**: CLI `gws-account` (richiede autorizzazione esplicita di Nando prima di qualsiasi mutation).

Regole generali:
- **Fonte di verita**: il repository git. Nessun Google Doc e` una seconda fonte.
- **write_guard**: ogni `create`, `update`, `move`, `delete` o modifica permessi su Drive richiede **autorizzazione esplicita preventiva di Nando** sul comando `gws-account` e sui target.
- **Account**: sempre `gws-account work ...`; mai `gws` nudo. L'account si conferma una volta per task.
- **Drift**: il criterio e` `modifiedTime` (la `version` di Drive si incrementa anche senza modifiche al contenuto). Se il `modifiedTime` corrente differisce da quello registrato, qualcuno ha modificato il Doc fuori dal repo: recepire o scartare esplicitamente prima di un push.
- **Commenti**: i commenti aperti sono feedback da leggere e recepire nel markdown locale prima di un push. La sostituzione totale del corpo puo' far perdere gli anchor dei commenti.

## Direzione A: pubblicare un file markdown locale su Google Drive

**Quando**: Nando modifica un `.md` in `contenuti/` (o `research/`) e vuole portarlo sul Google Doc.

1. **Drift check** (obbligatorio, prima di tutto):
   ```bash
   python3 .opencode/skills/openrouter-gdrive/scripts/verifica-drift-gdrive.py \
     --manifest manifest-gdrive.yaml check
   ```
   - 0 drift, 0 errori -> procedi.
   - Se drift rilevato -> **NON proseguire**. Usa la direzione B per recepire/scartare, poi riprova.
2. **Prepara il markdown** (rimuove H1 e sezioni local-only, riscrive i link incrociati):
   ```bash
   node .opencode/skills/openrouter-gdrive/scripts/gen-md-gdrive.mjs \
     --all --out-dir /tmp/openrouter-gdrive
   ```
   Oppure un solo file: `--source contenuti/<file>.md --out /tmp/<file>.md`.
3. **Anteprima** (opzionale, `--dry-run` valida localmente):
   ```bash
   gws-account work drive files update \
     --params '{"fileId":"<file_id>","fields":"id,name,mimeType,version,modifiedTime"}' \
     --upload <file>.md --upload-content-type text/markdown --dry-run
   ```
   Nota: `--upload` accetta solo path dentro la working directory del comando.
4. **Autorizzazione di Nando** sul comando e sui target (write_guard).
5. **Push effettivo** (sostituisce il corpo del Doc, resta un Google Doc):
   ```bash
   gws-account work drive files update \
     --params '{"fileId":"<file_id>","fields":"id,name,mimeType,version,modifiedTime"}' \
     --upload <file>.md --upload-content-type text/markdown
   ```
6. **Read-back**: esporta il Doc e verifica il contenuto:
   ```bash
   gws-account work drive files export \
     --params '{"fileId":"<file_id>","mimeType":"text/markdown"}' --output /tmp/readback.md
   ```
7. **Registra la pubblicazione**:
   ```bash
   python3 .opencode/skills/openrouter-gdrive/scripts/verifica-drift-gdrive.py \
     --manifest manifest-gdrive.yaml snapshot save --target <target_key> --publish
   ```
8. **Drift check finale** -> 0 drift. **Commit git**.

### Nuovo documento

Creare il Doc dal markdown e registrare `file_id` nel manifest:
```bash
gws-account work drive files create \
  --params '{"fields":"id,name,mimeType,version"}' \
  --json '{"name":"<Titolo>","mimeType":"application/vnd.google-apps.document","parents":["1bGRMC7V0k2kfulbsC-IUWVdOoYsVfUT1"]}' \
  --upload <file>.md --upload-content-type text/markdown
```

## Direzione B: ricevere/modificare da Google Drive (aggiornare il locale)

**Quando**: Nando (o un collega) ha modificato un Google Doc e vuole che il markdown locale lo rifletta.

1. **Drift check**:
   ```bash
   python3 .opencode/skills/openrouter-gdrive/scripts/verifica-drift-gdrive.py \
     --manifest manifest-gdrive.yaml check --target <target_key>
   ```
2. **Salva la baseline corrente** (esporta il Doc e registra `modified_time`/`drive_version`):
   ```bash
   python3 .opencode/skills/openrouter-gdrive/scripts/verifica-drift-gdrive.py \
     --manifest manifest-gdrive.yaml snapshot save --target <target_key>
   ```
3. **Leggi i commenti aperti** e recepiscili nel markdown:
   ```bash
   gws-account work drive comments list \
     --params '{"fileId":"<file_id>","fields":"comments(id,content,resolved,quotedFileContent(value),author(displayName))","pageSize":100}'
   ```
4. **Diff** fra baseline e pagina corrente (testo normalizzato):
   ```bash
   python3 .opencode/skills/openrouter-gdrive/scripts/verifica-drift-gdrive.py \
     --manifest manifest-gdrive.yaml diff --target <target_key>
   ```
5. **Riconcilia nel markdown locale** (`contenuti/`), includendo i commenti rilevanti.
6. **Verifica i link** del generato rispetto alla baseline:
   ```bash
   node .opencode/skills/openrouter-gdrive/scripts/gen-md-gdrive.mjs --verify <target_key>
   ```
7. **Reset della baseline** (locale e Drive di nuovo allineati):
   ```bash
   python3 .opencode/skills/openrouter-gdrive/scripts/verifica-drift-gdrive.py \
     --manifest manifest-gdrive.yaml snapshot save --target <target_key> --force
   ```
8. **Drift check finale** -> 0 drift. **Commit git**.

## Strumenti

| Tool | Dove | Comando |
|------|------|---------|
| Generatore markdown | `scripts/gen-md-gdrive.mjs` | `node gen-md-gdrive.mjs --all --out-dir /tmp/openrouter-gdrive` |
| Drift check | `scripts/verifica-drift-gdrive.py` | `python3 verifica-drift-gdrive.py --manifest manifest-gdrive.yaml check` |
| Baseline | stesso script | `snapshot save --target <key> [--publish] [--force] [--all]` |
| Diff documento | stesso script | `diff --target <key>` |
| Push Drive | `gws-account` | `gws-account work drive files update --params '{"fileId":"<id>"}' --upload <md> --upload-content-type text/markdown` |
| Export Drive | `gws-account` | `gws-account work drive files export --params '{"fileId":"<id>","mimeType":"text/markdown"}' --output <md>` |
| Commenti | `gws-account` | `gws-account work drive comments list --params '{"fileId":"<id>"}'` |

## Regole critiche

- **Non sovrascrivere mai** una modifica esterna senza averla prima recepita o scartata esplicitamente (decisione di Nando).
- **Titoli**: il titolo e` il nome del Google Doc; l'H1 locale viene rimosso dal generatore.
- **Link relativi**: nel markdown pubblicato non restano mai link relativi tra documenti; il generatore li riscrive con gli URL Google Docs del manifest.
- **Sezione `CONFLUENCE-LOCAL-ONLY`**: interna al repo, non si pubblica.
- **Commenti**: leggerli prima del push; la sostituzione totale del corpo puo' far perdere gli anchor.
- **Linguaggio italiano** per prosa e artefatti; inglese per keyword tecniche.
- **Decisioni**: se una modifica al processo o al manifest e` significativa, registrare una riga nel Decision Log con codice `DO-` (Decisione OpenRouter).

## Vedi anche

- `AGENTS.md` (root del repo) — contesto e routing delle skill disponibili.
- `manifest-gdrive.yaml` — control plane.
- `snapshots-gdrive/` — baseline markdown esportate dai Google Docs.
- Skill `openrouter-confluence` — il target Confluence sugli stessi sorgenti markdown.
