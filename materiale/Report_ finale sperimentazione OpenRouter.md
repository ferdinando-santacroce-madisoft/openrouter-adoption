# **Report finale: sperimentazione OpenRouter**

**Proposta di adozione di OpenRouter come AI Gateway aziendale**

| Campo | Valore |
| :---- | :---- |
| **Data** | 26/08/2026 |
| **Autore / Owner** | Ferdinando Santacroce |
| **Responsabile Iniziativa (PM/EM)** | Ferdinando Santacroce |
| **Destinatario** | Francesco Trucchia (CTO) |
| **Stato** | Bozza |
| **Riferimenti** | [Pitch adozione OpenRouter](https://docs.google.com/document/d/1cJzlOBfJdFqVby6GiRHPNTsg2NwZghfOv2pwXwBHjxI/edit?tab=t.0) · [SSR adozione OpenRouter](SSR_%20adozione%20OpenRouter.md) |

---

## 1. Scorecard di sintesi

| # | Obiettivo / KPI | Target | Risultato                                                    | Esito             |
| :---- | :---- | :---- |:-------------------------------------------------------------|:------------------|
| 1 | Riduzione tempi sui task di refactoring | -20% | Riduzioni osservate fino al 60% su scrittura test (PRO-1128) | 🟢                |
| 2 | Costo per sviluppatore dopo il rollout | ≤ 20$/mese/dev | Spesa media in sperimentazione: ≤ 20$/mese/dev               | Budget rispettato |
| 3 | Conformità privacy (routing EU + ZDR) | 100% | ZDR operativo; routing EU in attivazione                     | 🟡                |
| 4 | Accesso a modelli Open Weights di frontiera | Si | DeepSeek V4, GLM 5.2, Kimi 3, Sonnet 4.5 testati             | 🟢                |
| 5 | Intercambiabilità dei modelli (no vendor lock-in) | Verificata | Confermata nei flussi reali                                  |                 |

> **Sintesi:** la sperimentazione ha confermato le attese del pitch. L'AI gateway OpenRouter ha prodotto evidenze quantitative e qualitative concrete nei flussi di sviluppo reali (test, feature, refactoring, debugging, onboarding su codebase ignote), con costi per task nettamente inferiori rispetto al fornitore attuale. **Raccomandazione: procedere al rollout**, con le condizioni di sicurezza già approvate e il piano di adozione descritto in sezione 13.

---

## 2. Contesto e obiettivi

### 2.1 Contesto

La sperimentazione si colloca nella roadmap "Verso Nuvola 3.0", con l'obiettivo di rendere i team indipendenti e modernizzare l'architettura del monolite (Engineering Tech Strategy 2026-2028, Investment Category: **Strategic**). GitHub Copilot vincolava i team a un ecosistema rigido con modelli predefiniti e scarsa visibilità sui consumi, rendendo necessario valutare un gateway AI unificato con accesso ai migliori LLM Open Weights di frontiera.

### 2.2 Obiettivi della sperimentazione

1. Verificare l'efficacia di OpenRouter nei flussi reali di sviluppo (IDE, estensioni, script CLI, harness agentici).
2. Misurare impatto e costi attraverso classificatori automatici configurati sul gateway.
3. Validare la conformità (EU residency, Zero Data Retention) insieme al Team IT & CyberSecurity.
4. Confrontare il modello di consumo con GitHub Copilot (durata abbonamento, costi, flessibilità).
5. Produrre dati e impressioni di campo per la decisione di rollout.

### 2.3 Stakeholder coinvolti
 
| Ruolo | Nome                                                                                                     | Coinvolgimento |
| :---- |:---------------------------------------------------------------------------------------------------------| :---- |
| Owner | Ferdinando Santacroce                                                                                    | Setup, metriche, coordinamento |
| Team di sviluppo | Davide Fossacecchi, Federico Bartoli, Massimiliano Conforti, Anders Jipwouo, Marco Martorana, Lorenzo Piersante | Utilizzo e valutazione modelli |
| CTO | Francesco Trucchia                                                                                       | Monitoraggio, requisiti metriche, decisione finale |
| IT-Security | Pasquale Siciliano                                                                                       | Valutazione sicurezza (IS-313), direttive compliance |

---

## 3. Metodologia di misurazione

La sperimentazione ha usato i **classificatori** di OpenRouter (feature in beta) per taggare automaticamente ogni generazione LLM e aggregare metriche sul tipo di utilizzo. I classificatori operano sulle **generazioni** (non sui prompt), e solo in ingresso: non memorizzano né espongono il contenuto delle conversazioni.

### 3.1 Classificatori configurati

| Classificatore | Scopo | Ispirazione |
| :---- | :---- | :---- |
| **Autonomy Level** | Livello di autonomia agentica dell'interazione, da L0 (manuale) a L5 (orchestrazione full) | Framework di [Addy Osmani](https://addyo.substack.com/p/agentic-autonomy-levels) (L0-L5) |
| **Engineering Work** | Categoria di lavoro ingegneristico (feature, refactoring, bug fixing, test, ecc.) | Tassonomia interna |

I classificatori sono stati impostati il 05/08/2026 e la raccolta dati copre il periodo **27/07/2026 → 26/08/2026** (workspace `madisoft-test`).

### 3.2 Limite metodologico dichiarato

Durante la raccolta è emerso che il classificatore **Autonomy Level tendeva a sovrastimare il livello di autonomia** (segnalazione di Davide Fossacecchi il 12/08: una sessione guidata strettamente dal dev veniva classificata L3 invece di L2). Il system prompt del classificatore è stato aggiornato il 17/08. Le metriche vanno quindi lette come indicazione di tendenza, non come misura assoluta: riportiamo il bias per trasparenza.

---

## 4. Come abbiamo usato OpenRouter

### 4.1 Setup dell'organizzazione

- Account organizzazione aziendale attivato il 14/07/2026; invito dei partecipanti nel canale `prj-openrouter`.
- Workspace principale di sperimentazione: `madisoft-test`, con chiavi API dedicate per partecipante e **guardrails economici settimanali** per utente.
- Endpoint standardizzato compatibile con OpenAI SDK, integrato in **OpenCode** (con LSP abilitati), estensioni e script CLI.

### 4.2 Workspace e governance

| Workspace | Scopo | Note |
| :---- | :---- | :---- |
| `Default Workspace` | Workspace di default OpenRouter | Chiavi disattivate a fine luglio: nessun guardrail associato |
| `madisoft-test` | Sperimentazione team | Chiavi dedicate, guardrails settimanali, metriche classifier |

*Apprendimento chiave della governance: i guardrails vengono ereditati dalle chiavi solo se configurati sul workspace corretto; il workspace di default va bloccato a costo zero.*

### 4.3 Modelli utilizzati

| Modello | Caso d'uso prevalente | Note dal campo |
| :---- | :---- | :---- |
| DeepSeek V4 Flash (e 0731) | Lavoro quotidiano, planning, refactoring | Economico e produttivo; il preferito dal gruppo |
| DeepSeek V4 Pro | Sessione lunga a basso costo | 15 centesimi per un pomeriggio di lavoro |
| GLM 5.2 | Confronto qualitativo su task complessi | Valutato al pari di modelli premium |
| Kimi 3 | Frontend, review di PR corpose | Molto forte su FE (screen/figma); episodi di interruzione a metà lavoro |
| Sonnet 4.5 | Test spot ad alta reattività | Più costoso; valutazione non favorevole per l'uso quotidiano |
| Gemini 3.5 Flash Light | Subagent in OpenCode | Richiamato di default dagli harness; da vincolare via configurazione |

### 4.4 Strumenti integrati

- **OpenCode** (harness principale, con LSP abilitati per navigazione codice e formattazione corretta).
- API OpenAI-compatible per script CLI e automazioni.
- Integrazione AI coding in Swarmia valutata come follow-up (al momento Swarmia supporta nativamente Copilot/Claude Code/Cursor, non OpenRouter).

### 4.5 Periodo e partecipanti

- Canale attivo dal 14/07/2026; raccolta dati 27/07 → 26/08/2026.
- 6 sviluppatori coinvolti (D. Fossacecchi, F. Bartoli, M. Conforti, A. Jipwouo, M. Martorana, L. Piersante) con il CTO come osservatore attivo.

---

## 5. Esperimenti condotti

### 5.1 Casi d'uso reali con metriche quantitative

| Issue | Caso d'uso | Metrica | Autore |
| :---- | :---- | :---- | :---- |
| [PRO-1128](https://madisoft.atlassian.net/browse/PRO-1128) | Scrittura test (con repo in-memory e builder di entità) | **-60% tempi** | Davide F. |
| [PRO-1161](https://madisoft.atlassian.net/browse/PRO-1161) | Implementazione completa di test inclusi manuali | **1h** vs 2-2,5h a mano | Davide F. |
| [PRO-1187](https://madisoft.atlassian.net/browse/PRO-1187) | Test durante review; sblocco su problema tecnico reale (coda RabbitMQ creata dal consumer) | Sblocco immediato | Massimiliano C. |
| [PRO-1190](https://madisoft.atlassian.net/browse/PRO-1190) | PR 402 righe (con test) | **1h45m** vs 4h20m della issue gemella (319 righe); **spesa 0,66€** | Davide F. |
| [PRO-1271](https://madisoft.atlassian.net/browse/PRO-1271) | Test di 13 classi + 2 skill distillate | **1700 righe in 10h** (senza AI ~ doppio) | Davide F. |
| [PRO-1327](https://madisoft.atlassian.net/browse/PRO-1327) | Diagnosi fallimento test di integrazione non scritti da sé | **< 3 minuti** | Davide F. |
| [PRO-1164](https://madisoft.atlassian.net/browse/PRO-1164) | Blocco eliminazione/modifica pagamenti non DA PAGARE | PR [12173](https://github.com/madisoft/nuvola2/pull/12173) merged, +430/-68, 10 file | F. Santacroce / D. Fossacecchi |
| [PRO-1153](https://madisoft.atlassian.net/browse/PRO-1153) | Eliminazione massiva eventi solo se tutti DA PAGARE | PR [12180](https://github.com/madisoft/nuvola2/pull/12180) +927/-4, 13 file | Davide F. |
| [ATENA-1305](https://madisoft.atlassian.net/browse/ATENA-1305) | Feature flag salva in bozza su interpelli (frontend) | PR [77](https://github.com/madisoft/area-generale-frontend/pull/77) **merged 6 min dopo l'apertura**, +388/-291, 15 file | Federico B. |

### 5.2 Storie significative

- **PRO-1190 (0,66€ per una PR completa):** all'agente è stato passato lo SHA del commit della issue gemella e le differenze; i test sono stati scritti autonomamente, con un refactoring in più che era comunque un miglioramento. Spesa totale 0,66€.
- **PRO-1271 (1700 righe di test in 10h):** copertura di 13 classi fra integrazione e unitari, più 2 skill distillate per rendere più agevole il lavoro futuro e boilerplate riusabile.
- **Esperimento CTO (estrazione modulo `Comunicazioni`):** piano a barra verde generato in `plan mode` per l'estrazione del modulo. Considerato sensato sulla carta; giudizio condiviso: piano di massima da iterare punto per punto con ulteriori Plan.
- **PR review agentica (24/08):** esperimento di apertura PR da parte dell'agente e successiva review automatica. Feedback positivo: fornisce un punto stabile in cui assegnare le revisioni. La review di PR corpose (2400 righe) con Kimi 3 ha dato risultati superiori a GLM 5.2.
- **Mob/ensemble programming con l'AI (05/08):** sessione di 2h di sviluppo in coppia/ensemble usando l'AI, condivisa come buona pratica di trasferimento conoscenza.

---

## 6. Metriche raccolte

### 6.1 Autonomy Level (classificatore, ispirato a Addy Osmani L0-L5)

| Livello | % delle richieste |
| :---- | :---- |
| L2 - Partial Autonomy (task delimitati delegati) | **58,35%** |
| L3 - Conditional Autonomy (loop goal-driven) | 24,30% |
| L0 - Manual / Chat Direct | 12,85% |
| L1 - Human-Driven Assistive | 3,58% |
| L4 - High Autonomy (parallel delegation) | 0,93% |
| L5 - Full Autonomy | 0,00% |

> Lettura: la maggioranza del lavoro è delegata all'agente su task delimitati (L2), con un quarto delle sessioni in autonomia condizionata (L3). L'uso è prevalentemente agentico (unico livello pienamente "assistivo" L1: 3,58%). Il livello L4 è marginale: la delega parallela multi-agente è ancora sperimentale.

### 6.2 Tool loop (modalità di esecuzione)

| Modalità | % delle richieste |
| :---- | :---- |
| Loop read → write → execute | **79,59%** |
| Solo tool in sola lettura | 15,71% |
| Nessun tool | 4,69% |

### 6.3 Action scope (perimetro delle modifiche)

| Ambito | % delle richieste |
| :---- | :---- |
| Feature multi-file | **50,58%** |
| File singolo | 32,60% |
| Intero repository | 12,72% |
| Snippet di codice | 3,50% |
| Altro / infrastruttura | 0,59% |

### 6.4 Work type (tipo di lavoro)

| Categoria | % delle richieste |
| :---- | :---- |
| Feature development | **28,96%** |
| Refactoring | 24,23% |
| Bug fixing | 22,69% |
| Unit test generation | 8,23% |
| Research & exploration | 6,63% |
| Code quality | 5,26% |
| Documentazione | 1,17% |
| Migrazioni & upgrades | 0,90% |
| CI/CD & DevOps | 0,80% |
| Code review | 0,67% |
| Altro / Security / Data | 0,46% |

### 6.5 Costi

| Voce | Valore |
| :---- | :---- |
| Budget di trial disponibile | 200$ (2 mesi) |
| Spesa effettiva totale | **200$** (budget rispettato integralmente) |
| Costo medio per sviluppatore/mese | **≤ 20$** (allineato al target previsto dall'SSR) |
| Costi osservati nel campo | PRO-1190: 0,66€/PR · DeepSeek V4 Flash: ~0,06$ a sessione · DeepSeek V4 Pro: 0,15$ un pomeriggio · Kimi 3: ~0,30$ |
| Incidente di governance | 40$ in 2 giorni (GPT Sol, chiave nel workspace senza guardrail) |

> **Nota:** il budget di 200$ è stato rispettato integralmente. Eventuale breakdown dettagliato per modello/workspace dalla dashboard OpenRouter: [DA INSERIRE se disponibile].

---

## 7. Vantaggi e benefici osservati

Ogni vantaggio è accompagnato dall'evidenza raccolta.

- **Riduzione dei tempi sui test:** -60% su scrittura test (PRO-1128); 1h contro 2-2,5h manuali (PRO-1161); 1700 righe in 10h contro ~doppio senza AI (PRO-1271).
- **Velocità di consegna:** PR 402 righe in 1h45m contro 4h20m della gemella (PRO-1190); PR 77 merged 6 minuti dopo l'apertura (ATENA-1305).
- **Diagnostica rapida:** causa di test di integrazione falliti individuata in <3 minuti (PRO-1327); sblocco su problema reale RabbitMQ durante review (PRO-1187).
- **Costo per task competitivo:** 0,66€ per una PR completa (PRO-1190); modelli economici di alta qualità (DeepSeek V4 Flash/Pro).
- **Flessibilità assoluta:** cambio istantaneo di modello per task (scelta del modello giusto al momento giusto, no lock-in).
- **Governance e visibilità:** dashboard per workspace, guardrails economici, chiavi dedicate, classificatori per metriche di utilizzo.
- **Crescita di skill collettiva:** 2 skill distillate per il lavoro futuro (PRO-1271), momenti di mob programming con l'AI.

---

## 8. Voci dal campo

Citazioni selezionate dal canale `prj-openrouter` (14/07 → 26/08/2026).

### Professionali

> "Io uso parecchio Copilot per le sole review, perché per tutti gli altri utilizzi **dura troppo poco**." — Lorenzo Piersante

> "Se il prompt genera il codice, il prompt è conoscenza aziendale. Scrivere software è uno sport di gruppo, non individuale." — Francesco Trucchia (CTO)

> "Il prompt non è un artefatto come il codice: è il ragionamento grezzo. Se so che è attribuibile e leggibile, scrivo prompt presentabili invece che efficaci. Nel caso peggiore qualcuno smette di usare il tool aziendale e apre ChatGPT sul telefono: shadow AI." — Federico Bartoli

> "Il logging è un obbligo, non un'opzione. Come soggetto NIS2 essenziale dobbiamo garantire la tracciabilità delle operazioni." — Pasquale Siciliano (IT-Security)

> "Secondo me il classificatore sul livello di autonomia che abbiamo creato è troppo ottimistico." — Davide Fossacecchi

### Momenti di colore

> "Ho fatto una roba con Sonnet 4.5... **NON L'AVESSI MAI FATTO**. Ci pagavo Kimi con quei soldi e mi davano anche il resto." — Davide Fossacecchi

> "mi sa che c'è un bug sul prezzo del budget: vedo 6 euro al posto di 600 euro" — Massimiliano Conforti *(il guardrail economico a 600€ mostrava 6€)*

> "vai a casa umano" — Kimi 3 (riportato da Federico Bartoli)

> "Si sboccia!" — Ferdinando Santacroce *(sull'incidente dei 40$ in 2 giorni)*

---

## 9. Limiti e criticità evidenziati

- **Guardrails legati al workspace, non alle chiavi:** una chiave creata nel workspace sbagliato bypassa i guardrails economici. Incidente reale: 40$ spesi in 2 giorni con GPT Sol (auto-router) da un partecipante. Mitigato bloccando a zero il workspace di default.
- **Auto-router da usare con cautela:** il routing automatico ha selezionato GPT Sol, modello costoso. Da limitare o configurare con policy (white-list/black-list dei modelli).
- **Classificatore Autonomy Level ottimistico:** tendeva a sopravvalutare l'autonomia (L3 vs L2 reale); aggiornato il 17/08.
- **Qualità non omogenea dei provider:** per lo stesso modello la reattività varia a seconda del provider; episodi di degradazione percepita (DeepSeek V4 Flash "degradato" il 03/08).
- **Stabilità dei modelli nuovi:** Kimi 3 ha mostrato episodi di interruzione a metà lavoro con consumo di credito.
- **Modelli EU limitati e routing EU da abilitare:** la lista modelli con residenza EU è ridotta (dubbio emerso su Mistral) e il routing esclusivo EU è riservato a clienti Enterprise (attivazione richiesta in corso). Finché non è attivo, la selezione modelli compliant è vincolata.
- **Integrazione con GitHub/Swarmia assente:** la review direttamente su GitHub (come Copilot) non è nativa; Swarmia non espone integrazione per OpenRouter (da costruire).
- **Repo di grandi dimensioni:** su Nuvola (15.000 file) l'incidenza del contesto è significativa e pesa sui consumi.

---

## 10. Confronto con GitHub Copilot (fornitore attuale)

### 10.1 Tabella comparativa

| Criterio | GitHub Copilot | OpenRouter | Note / Evidenze |
| :---- | :---- | :---- | :---- |
| Modelli disponibili | Predefiniti, chiusi | 400+ (Open Weights di frontiera inclusi) | DeepSeek, GLM, Kimi testati in produzione |
| Pricing | Abbonamento a consumo che si esaurisce | Pay-as-you-go, spesa proporzionata all'uso reale | PRO-1190: 0,66€/PR |
| Durata abbonamento | **Esaurito in poche ore di lavoro**: oltre 1-1,5 ore al giorno di uso agentico i crediti finiscono prima del rinnovo mensile, anche sui modelli meno costosi | Uso elastico, spesa proporzionata all'uso reale | Confermato nel canale ("per tutti gli altri utilizzi dura troppo poco") |
| Flessibilità del modello | Bloccato | Intercambiabilità istantanea | Modello scelto per task |
| Controllo costi | Scarsa visibilità | Workspace, budget policy, guardrails con blocchi automatici | Incidente 40$ → guardrails |
| Back-office / governance | Ambiente utente chiuso | Console completa: seats, cap, guardrail, classificatori | Requisito MoSCoW M |
| Review su GitHub | Nativa | Non nativa (si replica con agenti/action custom) | Gap noto |
| Data residency / compliance | [DA INSERIRE] | EU API + ZDR contrattuale (DPA) | IS-313 compliant con riserva |

### 10.2 Evidenza del problema principale

Il difetto più rilevante di GitHub Copilot per Madisoft è la **durata dell'abbonamento**: i crediti mensili vengono esauriti in **poche ore** di lavoro agentico. I programmatori riportano che superando 1-1,5 ore al giorno di utilizzo i crediti finiscono prima ancora del rinnovo mensile, anche impiegando i modelli meno capaci (quelli che consumano meno crediti). Il tool è quindi di fatto poco utilizzabile per l'uso quotidiano continuativo e resta conveniente solo per attività limitate (come le review, come testimoniato nel canale). Il confronto quantitativo è reso evidente dal caso PRO-1190 vs la sua gemella PRO-1156 (stessa tipologia di issue, test generati con Copilot): con OpenRouter una PR completa da 402 righe è costata **0,66€** in 1h45m.

---

## 11. Cosa abbiamo imparato su OpenRouter

| Lezione | Impatto concreto |
| :---- | :---- |
| **Guardrails a zero sul workspace di default** | Previene lo sforamento incontrollato (incidente 40$ con GPT Sol) |
| **Workspace = team** | Dashboard di utilizzo per team con log per team (requisito CTO: "l'unità minima è il team") |
| **Chiavi API dedicate per utente/workspace** | Isolamento ambienti e attribuzione dei consumi |
| **Auto-router con policy** | Evita la selezione di modelli costosi (GPT Sol); meglio white-list o `:floor` |
| **`:floor` per il routing sul provider più economico** | Abbattimento dinamico dei costi rispetto ai prezzi fissi dei competitor |
| **Scelta del modello per task** | DeepSeek V4 Flash per il quotidiano, Kimi 3 per FE/review corpose, GLM 5.2 per confronti complessi |
| **Classificatori per metriche di utilizzo** | Misurazione del tipo di utilizzo senza esporre i prompt (privacy) |
| **Preferire modelli economici e produttivi** | DeepSeek V4 Flash 0731 "ancora più economico e produttivo"; Sonnet 4.5 non conveniente per l'uso quotidiano |

---

## 12. Sicurezza & Compliance

### 12.1 Stato

- **IS-313 — Valutazione sicurezza OpenRouter Enterprise:** Done (Pasquale Siciliano).
- **Pagina "Qualifica Fornitore e DPIA - OpenRouter Enterprise"** (codice PG-PUR-01/OR-2026, rev. 1.0, 05/08/2026): **approvata, stato Green**.
- Esito: compliant (con riserva) per l'utilizzo dello strumento.

### 12.2 Direttive obbligatorie (da applicare a monte)

1. **Data Residency:** configurare esclusivamente le region EU per l'elaborazione dei dati.
2. **Prevenzione leak:** `.cbmignore`/`.gitignore` per escludere file `.env`, chiavi SSH, certificati e dati personali dal transito verso l'IA.
3. **Zero Data Retention:** selezionare esclusivamente i modelli che supportano la ZDR contrattuale.

### 12.3 Stato di avanzamento e temi aperti

- **ZDR:** già operativo.
- **Routing esclusivo EU:** riservato a clienti Enterprise; richiesta di attivazione inoltrata il 06/08/2026 (in corso). Finché non è attivo, la selezione dei modelli compliant è limitata.
- **I/O logging:** al momento non applicabile all'endpoint EU (risolto a monte). Dibattito aperto su logging e monitoraggio: obbligo di tracciabilità NIS2 (IT-Security) vs rischi di privacy e di alterazione del comportamento (team). Decisione da formalizzare.
- **Sandboxing degli agenti:** valutazione futura per isolare l'esecuzione degli agenti dal file system locale.

---

## 13. Piano di adozione (in caso di approvazione)

### 13.1 Fasi

| Fase | Attività | Timeline | Responsabile |
| :---- | :---- | :---- | :---- |
| 1 | Kickoff, comunicazione e aggiornamento guardrails (default workspace a zero, workspace per team) | Settembre 2026 | F. Santacroce |
| 2 | Onboarding degli sviluppatori (chiavi dedicate, tooling OpenCode, policy modello) | Settembre 2026 | F. Santacroce |
| 3 | Spostamento del budget ricorrente 20$/mese/dev da Copilot verso OpenRouter | Da rollout | F. Santacroce |
| 4 | Attivazione routing EU esclusivo e verifica compliance ZDR/DPIA | In corso | F. Santacroce + IT-Security |
| 5 | Configurazione integrazione metriche (Swarmia custom / dashboard per team) | Ottobre 2026 | Team + CTO |
| 6 | Monitoraggio consumi e checkpoint mensile (metriche classifier + costi) | Continuo | F. Santacroce |

### 13.2 Budget richiesto

- Costo di avvio: già sostenuto (trial 200$, speso integralmente come previsto).
- Costo ricorrente: ~20$/mese/dev (allineato al target previsto dall'SSR).

### 13.3 Metriche di successo post-adozione

- Mantenimento della spesa ≤ 20$/mese/dev.
- Riduzione dei tempi sui task di refactoring (target -20%, con riduzioni già osservate fino al 60% sui test).
- Conformità EU/ZDR al 100%.
- Soddisfazione sviluppatori (survey a 90 giorni).
- Adozione per team visibile su dashboard (workspace per team).

### 13.4 Rischi residui e mitigazioni

| Rischio | Mitigazione |
| :---- | :---- |
| Sforamenti di spesa per configurazioni errate | Guardrails a zero sul default workspace; verifica ereditarietà chiavi |
| Selezione modelli costosi via auto-router | Policy/white-list modelli, uso di `:floor` |
| Disomogeneità provider sullo stesso modello | Test di reattività prima dell'adozione a livello di team |
| Limiti modelli EU | Attivazione routing EU Enterprise; monitoraggio listino EU |
| Conformità logging (NIS2 vs privacy) | Decisione formale condivisa con IT-Security/HR |

---

## 14. Richiesta di approvazione al CTO

> **Richiesta:** approvazione del piano di adozione descritto in sezione 13 e del budget associato, con spostamento del budget ricorrente attualmente allocato su GitHub Copilot verso OpenRouter.

| Ruolo | Nome | Decisione | Data / Firma |
| :---- | :---- | :---- | :---- |
| Owner | Ferdinando Santacroce | Proponente | 26/08/2026 |
| CTO | Francesco Trucchia | [DA INSERIRE] | [DA INSERIRE] |
| IT & CyberSecurity | Pasquale Siciliano | [DA INSERIRE] | [DA INSERIRE] |

---

## 15. Riferimenti

- [Pitch: adozione OpenRouter](https://docs.google.com/document/d/1cJzlOBfJdFqVby6GiRHPNTsg2NwZghfOv2pwXwBHjxI/edit?tab=t.0)
- [SSR: adozione OpenRouter](SSR_%20adozione%20OpenRouter.md)
- [Offerta OpenRouter per Madisoft](https://docs.google.com/document/d/1UBShAQGmeq83RXyu8H53sxSQqabjQFiO)
- [DPA OpenRouter (EU Processing Commitments)](https://docs.google.com/document/d/1_mKzFKAQ0Ta5tnMwM0VXzGwGpe8BhbFD/edit?usp=drive_link&ouid=114031065277990723110&rtpof=true&sd=true)
- [IS-313 — Valutazione sicurezza OpenRouter Enterprise](https://madisoft.atlassian.net/browse/IS-313)
- [Qualifica Fornitore e DPIA - OpenRouter Enterprise (Confluence)](https://madisoft.atlassian.net/wiki/spaces/TIS/pages/528023559/Qualifica+Fornitore+e+DPIA+-+OpenRouter+Enterprise)
- [OpenRouter Documentation Portal](https://openrouter.ai/docs/)
- Canale Slack `prj-openrouter` (14/07 → 26/08/2026)
- Metriche classifier (`.nando/openrouter/metriche-classifer`)
- Casi di utilizzo AI (`.nando/openrouter/Casi Utilizzo AI - Foglio1.csv`)
- Epica Jira: [DA INSERIRE: link epica]
- Iniziativa Swarmia: [DA INSERIRE: link Swarmia]

---

## Appendice A — Mappa partecipanti

| Persona | Ruolo/Team | Ruolo nella sperimentazione |
| :---- | :---- | :---- |
| Ferdinando Santacroce | [AMET] Staff Engineer | Owner, setup, metriche |
| Davide Fossacecchi | Dev backend | Utilizzo intensivo, casi PRO-1128/1161/1190/1271/1327/1153 |
| Federico Bartoli | [Atena] Frontend dev | Utilizzo frontend, ATENA-1305 (PR 77) |
| Massimiliano Conforti | Dev | PRO-1187, valutazioni modelli |
| Anders Jipwouo | Dev | Partecipante |
| Marco Martorana | Dev | Incidente guardrails 40$ (lezione appresa) |
| Lorenzo Piersante | [Atena] Backend dev | Confronto Copilot (review), considerazioni privacy |
| Francesco Trucchia | CTO | Requisiti metriche, esperimento Comunicazioni, decisione |
| Pasquale Siciliano | IT-Security | IS-313, direttive compliance |

## Appendice B — Dettaglio metriche CSV (valori grezzi)

| Autonomy Level | Value | % | Tool Loop | Value | % |
| :---- | :---- | :---- | :---- | :---- | :---- |
| L2_Partial | 24.231919 | 58.35 | read_write_execute_loop | 33.056226 | 79.59 |
| L3_Conditional | 10.090247 | 24.30 | read_only_tools | 6.526626 | 15.71 |
| L0_Manual | 5.336758 | 12.85 | no_tools | 1.948346 | 4.69 |
| L1_Assistive | 1.485288 | 3.58 | | | |
| L4_High | 0.386986 | 0.93 | | | |

| Action Scope | Value | % | Work Type | Value | % |
| :---- | :---- | :---- | :---- | :---- | :---- |
| multi_file_feature | 21.007974 | 50.58 | Feature development | 12.099488 | 28.96 |
| single_file | 13.539399 | 32.60 | Refactoring | 10.122866 | 24.23 |
| entire_repository | 5.283542 | 12.72 | Bug fixing | 9.480858 | 22.69 |
| snippet_code | 1.452966 | 3.50 | Unit test generation | 3.439004 | 8.23 |
| Other | 0.241332 | 0.58 | Research & exploration | 2.769786 | 6.63 |
| system_infrastructure | 0.005985 | 0.01 | Code quality | 2.19802 | 5.26 |
| | | | Documentazione | 0.486754 | 1.17 |
| | | | Migrations & upgrades | 0.377261 | 0.90 |
| | | | CI/CD & DevOps | 0.334493 | 0.80 |
| | | | Code review | 0.280356 | 0.67 |
| | | | Other | 0.154824 | 0.37 |
| | | | Security | 0.027821 | 0.07 |
| | | | Data & automation | 0.00939 | 0.02 |
