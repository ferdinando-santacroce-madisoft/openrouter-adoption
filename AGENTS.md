# Repo OpenRouter Adoption — contesto per l'agente

## Identita

Questo repo gestisce i documenti della **selezione software OpenRouter** (SSR, Pitch, Report finale) e la loro pubblicazione su Confluence e Google Drive. I sorgenti markdown vivono in `contenuti/` (sorgente unica per entrambi i target) e in `research/` per gli appunti. Le pagine sono pubblicate nello spazio Confluence **TIS** (`madisoft.atlassian.net/wiki/spaces/TIS`) come figlie del database **Selezione Software** (`38142402`), sotto `Corporate IT` (`245596166`); i documenti collaborativi vivono nella cartella Drive **Adozione OpenRouter** (`1bGRMC7V0k2kfulbsC-IUWVdOoYsVfUT1`, account `work`).

## Impianto di sincronizzazione Confluence

- **Skill**: `openrouter-confluence` (`.opencode/skills/openrouter-confluence/SKILL.md`) — due direzioni:
  - **Locale -> Confluence**: drift check -> gen-body -> twg update (dry-run, autorizzazione, --yes) -> read-back -> snapshot --publish -> check -> commit.
  - **Confluence -> Locale**: drift check -> snapshot del corpo corrente -> confronto testo -> riconciliazione nel markdown -> verify -> snapshot --force -> check -> commit.
- **Control plane**: `manifest-confluence.yaml` (3 artifacts pubblicabili; spazio TIS; riga del database da aggiornare).
- **Generator**: `.opencode/skills/openrouter-confluence/scripts/gen-body-confluence.mjs` (Node, markdown-it + js-yaml). Trasforma il markdown in body HTML Confluence.
- **Drift check**: `.opencode/skills/openrouter-confluence/scripts/verifica-drift-confluence.py` (Python, ruamel.yaml). Sottocomandi `check`, `snapshot save [--publish] [--force] [--all]`, `diff`. Parametrizzabile con `--manifest`, `--snapshot-dir`, `--label`.
- **Snapshot**: `snapshots-confluence/*.html` (corpo HTML pubblicato e baseline con versioni + sha256).

## Impianto di sincronizzazione Google Drive

- **Skill**: `openrouter-gdrive` (`.opencode/skills/openrouter-gdrive/SKILL.md`) — due direzioni:
  - **Locale -> Drive**: drift check -> gen-md -> gws update (dry-run, autorizzazione) -> read-back -> snapshot --publish -> check -> commit.
  - **Drive -> Locale**: drift check -> snapshot del markdown corrente + lettura commenti -> diff testuale -> riconciliazione nel markdown -> verify -> snapshot --force -> check -> commit.
- **Control plane**: `manifest-gdrive.yaml` (4 artifacts; cartella Drive; account `work`).
- **Generator**: `.opencode/skills/openrouter-gdrive/scripts/gen-md-gdrive.mjs` (Node, js-yaml). Prepara il markdown (rimuove H1 e sezioni local-only, riscrive i link incrociati verso gli URL Drive).
- **Drift check**: `.opencode/skills/openrouter-gdrive/scripts/verifica-drift-gdrive.py` (Python, ruamel.yaml). Sottocomandi `check`, `snapshot save [--publish] [--force] [--all]`, `diff`. Criterio di drift: `modifiedTime` (non la `version`).
- **Baseline**: `snapshots-gdrive/*.md` (markdown esportato dai Google Docs + `modified_time` + sha256).

## Skill disponibili

Oltre a `openrouter-confluence`, in questo repo puoi usare queste skill per **recuperare dati**. Caricale quando ti serve il contesto corrispondente:

- **nuvola-slack**: accesso ai messaggi su Slack (canale `prj-openrouter`).
- **twg**: accesso a Confluence e Jira. Usala sia per recuperare dati sia, in particolare, per eseguire gli **aggiornamenti su Confluence**.
- **gws** (Google Workspace): accesso ai file su Google Drive (Docs, Sheets, ecc.).

## Risorse esterne

- Vedi `RISORSE.md`: indice dei link operativi (database Selezione Software, canale Slack, pagine Confluence chiave, documenti Google di supporto).

## Regole di scrittura

- **Linguaggio italiano** per prosa e artefatti; inglese per keyword tecniche.
- **Mai em-dash (`—`) in prosa**: usa virgola, due punti o punto e virgola.
- **Titoli**: usa `: ` dopo il titolo (`# Titolo: sottotitolo`), mai Title Case.
- **write_guard**: nessuna scrittura su Confluence senza autorizzazione esplicita preventiva di Nando sul comando TWG e sui target.

## Workflow tipico

1. `drift check` -> 0 drift, 0 errori.
2. Modifica il `.md` in `contenuti/`.
3. `gen-body` -> genera il body HTML.
4. `twg update --dry-run` -> autorizzazione Nando -> `twg update --yes`.
5. `snapshot save --target <key> --publish` -> `check` -> commit.

## Target Confluence

- **Spazio**: TIS (`245432324`).
- **Database Selezione Software**: `38142402` (figlio di Corporate IT `245596166`).
  - Riga **Open Router** (`id 6`): campo `Documento` da puntare alla pagina SSR.
- **Pagine di riferimento**: Qualifica Fornitore e DPIA OpenRouter Enterprise (`528023559`); altri SSR sorell` (MCP coding agent `414875649` = MAD.TIS.SSR.01, SAST `611254289` = MAD.TIS.SSR.02).
