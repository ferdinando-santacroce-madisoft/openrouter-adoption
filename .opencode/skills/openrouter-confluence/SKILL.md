---
name: openrouter-confluence
description: >-
  Sincronizzazione bidirezionale tra i documenti locali della selezione
  software OpenRouter (spazio Confluence TIS, `madisoft.atlassian.net/wiki/spaces/TIS`,
  database "Selezione Software") e Confluence. Gestisce la pubblicazione
  locale -> Confluence e la ricezione/modifica da Confluence -> locale, con
  tutti i check e le verifiche del caso (drift, snapshot, read-back). Usa
  quando devi pubblicare un aggiornamento su Confluence, ricevere o
  riconciliare modifiche fatte direttamente su Confluence, o verificare lo
  stato di allineamento delle pagine OpenRouter.
---

# OpenRouter <-> Confluence: sincronizzazione bidirezionale

## Contesto

- **Repo**: `openrouter-adoption` — i sorgenti markdown vivono in `contenuti/`.
- **Spazio Confluence**: `TIS` (`madisoft.atlassian.net/wiki/spaces/TIS`), database **"Selezione Software"** (`38142402`) sotto `Corporate IT` (`245596166`).
- **Control plane**: `manifest-confluence.yaml` (artifacts, content_id, runtime fields).
- **Generator**: `.opencode/skills/openrouter-confluence/scripts/gen-body-confluence.mjs`.
- **Drift check**: `.opencode/skills/openrouter-confluence/scripts/verifica-drift-confluence.py`.
- **Scrittura Confluence**: CLI `twg` (richiede autorizzazione esplicita di Nando prima di qualsiasi `--yes`).

Regole generali:
- **Fonte di verita**: il repository git. Nessuna pagina Confluence e` una seconda fonte.
- **write_guard**: ogni `create`, `update`, `move`, `label`, `permission change`, `archive` o `delete` su Confluence richiede **autorizzazione esplicita preventiva di Nando** sul comando TWG e sui target.
- **Hard block sul drift**: se la versione Confluence di una pagina e` maggiore di `confluence_version` nel manifest, qualcuno ha modificato la pagina fuori dal repo. Prima di qualsiasi update locale, riconciliare o scartare esplicitamente la modifica esterna.

## Direzione A: pubblicare un file markdown locale su Confluence

**Quando**: Nando modifica un `.md` in `contenuti/` e vuole portarlo su Confluence.

1. **Drift check** (obbligatorio, prima di tutto):
   ```bash
   python3 .opencode/skills/openrouter-confluence/scripts/verifica-drift-confluence.py \
     --manifest manifest-confluence.yaml check
   ```
   - 0 drift, 0 errori -> procedi.
   - Se drift rilevato -> **NON proseguire**. Usa la direzione B per ricevere/modificare il locale, poi riprova.
2. **Genera il body** dal sorgente:
   ```bash
   node .opencode/skills/openrouter-confluence/scripts/gen-body-confluence.mjs \
     --source contenuti/<file>.md --out /tmp/<file>.html
   ```
   Oppure tutti:
   ```bash
   node .opencode/skills/openrouter-confluence/scripts/gen-body-confluence.mjs --all --out-dir /tmp/openrouter-bodies
   ```
3. **Dry-run** (prova di scrittura, nessun effetto):
   ```bash
   twg confluence content get <content_id> -o json            # legge snapshotToken "v:N"
   twg confluence content update <content_id> --snapshot-token "v:N" \
     --body-file /tmp/<file>.html --format html --ack-body-formats --dry-run
   ```
4. **Autorizzazione di Nando** sul comando e sui target (write_guard).
5. **Update effettivo**:
   ```bash
   twg confluence content update <content_id> --snapshot-token "v:N" \
     --body-file /tmp/<file>.html --format html --ack-body-formats \
     --version-message "<messaggio>" --yes
   ```
6. **Read-back**: leggi la pagina aggiornata e verifica il contenuto.
7. **Registra la pubblicazione**:
   ```bash
   python3 .opencode/skills/openrouter-confluence/scripts/verifica-drift-confluence.py \
     --manifest manifest-confluence.yaml snapshot save --target <target_key> --publish
   ```
8. **Drift check finale**:
   ```bash
   python3 .opencode/skills/openrouter-confluence/scripts/verifica-drift-confluence.py \
     --manifest manifest-confluence.yaml check
   ```
9. **Commit git**: sorgente + manifest aggiornato + snapshot.

### Prima pubblicazione (create)

Le pagine non esistono ancora: si creano come figlie del database `Selezione Software` (`38142402`) con `twg confluence content create`. Dopo il create si registrano `content_id`, `url` e versione nel manifest, si rigenerano i body (cosi' i link incrociati risolvono agli URL Confluence) e si rifa' l'update. La riga `Open Router` (id `6`) del database si aggiorna con il campo `Documento` puntato alla pagina SSR.

## Direzione B: ricevere/modificare da Confluence (aggiornare il locale)

**Quando**: Nando ha modificato direttamente una pagina su Confluence e vuole che il markdown locale rifletta le modifiche.

1. **Drift check**:
   ```bash
   python3 .opencode/skills/openrouter-confluence/scripts/verifica-drift-confluence.py \
     --manifest manifest-confluence.yaml check --target <target_key>
   ```
   Se drift -> la pagina Confluence e` piu' aggiornata del locale.
2. **Leggi il corpo corrente** e il suo snapshot:
   ```bash
   python3 .opencode/skills/openrouter-confluence/scripts/verifica-drift-confluence.py \
     --manifest manifest-confluence.yaml snapshot save --target <target_key>
   ```
3. **Confronta** il corpo Confluence (snapshot `.html`) con il sorgente markdown locale:
   - Converti lo snapshot in testo (rimuovi tag HTML) e confrontalo con il markdown.
   - Identifica le differenze reali (ignora la resa markdown->HTML: liste, tabelle, checkbox).
4. **Riconcilia nel markdown locale**: modifica il `.md` di `contenuti/` per riflettere il contenuto Confluence.
5. **Rigenera e verifica**:
   ```bash
   node .opencode/skills/openrouter-confluence/scripts/gen-body-confluence.mjs \
     --verify <target_key>
   ```
   (deve dire `href identici allo snapshot pubblicato`).
6. **Reset della baseline** (il locale e Confluence sono di nuovo allineati):
   ```bash
   python3 .opencode/skills/openrouter-confluence/scripts/verifica-drift-confluence.py \
     --manifest manifest-confluence.yaml snapshot save --target <target_key> --force
   ```
7. **Drift check finale** -> 0 drift.
8. **Commit git**.

## Strumenti

| Tool | Dove | Comando |
|------|------|---------|
| Generatore body | `scripts/gen-body-confluence.mjs` | `node gen-body-confluence.mjs --source <md> --out <html>` |
| Drift check | `scripts/verifica-drift-confluence.py` | `python3 verifica-drift-confluence.py --manifest manifest-confluence.yaml check` |
| Snapshot | stesso script | `snapshot save --target <key> [--publish] [--force] [--all]` |
| Diff pagina | stesso script | `snapshot diff --target <key>` |
| Scrittura Confluence | `twg` CLI | `twg confluence content update <id> --snapshot-token "v:N" --body-file <html> --format html --ack-body-formats` |

## Regole critiche

- **Non sovrascrivere mai** una modifica esterna senza averla prima recepita o scartata esplicitamente (decisione di Nando).
- **Titoli**: il titolo Confluence e separato dal body (l'H1 iniziale viene rimosso dal generatore).
- **Link relativi**: nel corpo pubblicato non restano mai href relativi; il generatore li riscrive con gli URL Confluence assoluti del manifest.
- **Chiavi Jira**: diventano link stabili `https://madisoft.atlassian.net/browse/<KEY>`.
- **Niente id sugli heading**: il formato di storage Confluence non li accetta.
- **Contenuto in `<pre>`/`<code>`**: non toccato dal generatore.
- **Sezione `CONFLUENCE-LOCAL-ONLY`**: interna al repo, non si pubblica.
- **Linguaggio italiano** per prosa e artefatti; inglese per keyword tecniche.
- **Decisioni**: se una modifica al processo o al manifest e` significativa, registrare una riga nel Decision Log con codice `DO-` (Decisione OpenRouter).

## Vedi anche

- `AGENTS.md` (root del repo) — contesto e routing delle skill disponibili per recuperare dati (`nuvola-slack`, `twg`, `gws`).
- `manifest-confluence.yaml` — control plane.
- `snapshots-confluence/` — corpo HTML pubblicato e baseline.
