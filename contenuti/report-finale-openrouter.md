# Report finale: sperimentazione OpenRouter

**Proposta di adozione di OpenRouter come AI Gateway aziendale**

---

| Campo | Valore |
|---|---|
| Data | 25/09/2026 (rev. 2.2) |
| Autore / Owner | Ferdinando Santacroce |
| Responsabile Iniziativa (PM/EM) | Ferdinando Santacroce |
| Destinatario | Francesco Trucchia (CTO) · Diego Moretti (CEO) |
| Stato | Approvato (12/10/2026) |
| Riferimenti | [Pitch adozione OpenRouter](pitch-adozione-openrouter.md) · [SSR adozione OpenRouter](ssr-adozione-openrouter.md) · [IS-313](https://madisoft.atlassian.net/browse/IS-313) · [Qualifica Fornitore e DPIA](https://madisoft.atlassian.net/wiki/spaces/TIS/pages/528023559) · [Epica Jira STAFF-118](https://madisoft.atlassian.net/browse/STAFF-118) |

---


## Sommario

**In una frase:** la sperimentazione di OpenRouter come gateway AI aziendale ha prodotto evidenze concrete di riduzione dei tempi, costi prevedibili e governabili, accesso ai migliori modelli open di frontiera, e piena compatibilità con i nostri vincoli di compliance europea. Raccomandazione: procedere al rollout, mantenendo il tetto di costo già previsto dal SSR.

### Cosa abbiamo fatto
Da luglio ad agosto 2026, 6 sviluppatori hanno usato OpenRouter nei flussi di sviluppo reali (test, feature, refactoring, debugging, onboarding su codebase sconosciute). Non una demo in laboratorio: lavoro vero su issue di produzione, con metriche misurate automaticamente da classificatori configurati sul gateway.

### Cosa abbiamo ottenuto
- **Tempi e output:** riduzione fino al **60%** sui task di scrittura test ([PRO-1128](https://madisoft.atlassian.net/browse/PRO-1128)); PR da 402 righe completata in **1h45m a 0,66€** contro le 4h20m della issue gemella ([PRO-1190](https://madisoft.atlassian.net/browse/PRO-1190) vs [PRO-1156](https://madisoft.atlassian.net/browse/PRO-1156)); frontend mai visto prima: PR in 1h senza onboarding ([PRO-1272](https://madisoft.atlassian.net/browse/PRO-1272)); 1700 righe di test in 10h ([PRO-1271](https://madisoft.atlassian.net/browse/PRO-1271)); diagnosi di test di integrazione falliti in **meno di 3 minuti** ([PRO-1327](https://madisoft.atlassian.net/browse/PRO-1327)); 33% di un'epica consegnato in un giorno ([PRO-1249](https://madisoft.atlassian.net/browse/PRO-1249)).
- **Costi prevedibili:** niente abbonamenti "a consumo che si esaurisce": si paga solo l'uso reale. Costi tipici: ~0,06$ a sessione (DeepSeek V4 Flash), 0,15$ per un pomeriggio di lavoro (V4 Pro), 0,66€ per una PR completa. La spesa media in sperimentazione è rimasta **≤ 20$/mese per sviluppatore**, coerente con il tetto approvato.
- **Flessibilità e anti lock-in:** cambio istantaneo di modello per task, scelta del modello giusto al momento giusto, nessun vincolo a un singolo vendor.
- **Governance reale:** dashboard per workspace, chiavi dedicate, guardrail economici con blocchi automatici, classificatori di utilizzo. Un incidente di governance (40$ in 2 giorni per una chiave in un workspace non presidiato) è servito da lezione ed è stato risolto bloccando a zero il workspace di default.
- **Compliance:** Zero Data Retention operativo; routing esclusivo EU disponibile con il passaggio al piano Business (71 modelli su 625 in regione EU, inclusi quelli usati); valutazione sicurezza [IS-313](https://madisoft.atlassian.net/browse/IS-313) e DPIA/Qualifica Fornitore approvate (Green) in data 05/08/2026.

### Cosa chiediamo (esito)
Il piano di adozione (sezione 13) e lo spostamento del budget ricorrente attuale (ammontare pari a ~20$/mese/dev su GitHub Copilot) verso OpenRouter sono stati **approvati in riunione il 12/10/2026** da CTO e CEO. Il costo di avvio (trial 200$) è già stato sostenuto e il budget è stato caricato dal CEO sul conto OpenRouter.

### Nota di trasparenza
L'incidente di governance (40$) e la qualità non omogenea di alcuni provider sono criticità gestite e documentate in sezione 9; il classificatore usato per le metriche è euristico e va letto come indicatore di tendenza (bias dichiarato in sezione 3.2).

---

## 1. Scorecard di sintesi

| # | Obiettivo / KPI | Target | Risultato | Esito |
|---|---|---|---|---|
| 1 | Riduzione tempi sui task di refactoring | -20% | Riduzioni osservate fino al 60% su scrittura test ([PRO-1128](https://madisoft.atlassian.net/browse/PRO-1128)); 33% epica in un giorno ([PRO-1249](https://madisoft.atlassian.net/browse/PRO-1249)) | 🟢 |
| 2 | Costo per sviluppatore dopo il rollout | ≤ 20$/mese/dev | Spesa trial totale $199.76 su 200$; ~22$/dev/mese osservato (incluso classificatore + incidente GPT-5.6 Sol) | 🟢 |
| 3 | Conformità privacy (routing EU + ZDR) | 100% | ZDR operativo; routing EU disponibile con il piano Business (71 modelli EU su 625, inclusi i principali) | 🟢 |
| 4 | Accesso a modelli Open Weights di frontiera | Sì | DeepSeek V4, GLM 5.2, Kimi 3, Sonnet 4.5 testati | 🟢 |
| 5 | Intercambiabilità dei modelli (no vendor lock-in) | Verificata | Confermata nei flussi reali | 🟢 |

**Sintesi:** la sperimentazione ha confermato le attese del pitch. L'AI gateway OpenRouter ha prodotto evidenze quantitative e qualitative concrete nei flussi di sviluppo reali, con costi per task nettamente inferiori rispetto al fornitore attuale. Raccomandazione: procedere al rollout con le condizioni di sicurezza già approvate e il piano descritto in sezione 13.

---

## 2. Contesto e obiettivi

### 2.1 Contesto
La sperimentazione si colloca nella roadmap "Verso Nuvola 3.0" (spazio Confluence [VN3](https://madisoft.atlassian.net/wiki/spaces/VN3)), con l'obiettivo di rendere i team indipendenti e modernizzare l'architettura del monolite (Engineering Tech Strategy 2026-2028, Investment Category: Strategic). GitHub Copilot vincolava i team a un ecosistema rigido con modelli predefiniti e scarsa visibilità sui consumi, rendendo necessario valutare un gateway AI unificato con accesso ai migliori LLM Open Weights di frontiera.

Le iniziative di indipendenza (spazio VN3 in Confluence: [Verso Nuvola3](https://madisoft.atlassian.net/wiki/spaces/VN3)) sono il terreno naturale in cui l'AI agentica può avere il maggiore impatto.

### 2.2 Obiettivi della sperimentazione
1. Verificare l'efficacia di OpenRouter nei flussi reali di sviluppo (IDE, estensioni, script CLI, harness agentici).
2. Misurare impatto e costi attraverso classificatori automatici configurati sul gateway.
3. Validare la conformità (EU residency, Zero Data Retention) insieme al Team IT & CyberSecurity.
4. Confrontare il modello di consumo con GitHub Copilot (durata abbonamento, costi, flessibilità).
5. Produrre dati e impressioni di campo per la decisione di rollout.

### 2.3 Stakeholder coinvolti
| Ruolo | Nome | Coinvolgimento |
|---|---|---|
| Owner | Ferdinando Santacroce | Setup, metriche, coordinamento |
| Team di sviluppo | Davide Fossacecchi, Federico Bartoli, Massimiliano Conforti, Anders Jipwouo, Marco Martorana, Lorenzo Piersante | Utilizzo e valutazione modelli |
| CTO | Francesco Trucchia | Monitoraggio, requisiti metriche, decisione finale |
| IT-Security | Pasquale Siciliano | Valutazione sicurezza ([IS-313](https://madisoft.atlassian.net/browse/IS-313)), direttive compliance |

---

## 3. Metodologia di misurazione

La sperimentazione ha usato i classificatori di OpenRouter (feature in beta) per taggare automaticamente ogni generazione LLM e aggregare metriche sul tipo di utilizzo. I classificatori operano sulle generazioni (non sui prompt) e solo in ingresso: non memorizzano né espongono il contenuto delle conversazioni.

### 3.1 Classificatori configurati
| Classificatore | Scopo | Ispirazione |
|---|---|---|
| Autonomy Level | Livello di autonomia agentica dell'interazione, da L0 (manuale) a L5 (orchestrazione full) | Framework di Addy Osmani (L0-L5) |
| Engineering Work | Categoria di lavoro ingegneristico (feature, refactoring, bug fixing, test, ecc.) | Tassonomia interna |

I classificatori sono stati impostati il 05/08/2026 e la raccolta dati copre il periodo 27/07/2026 → 26/08/2026 (workspace `madisoft-test`).

### 3.2 Limite metodologico dichiarato
Durante la raccolta è emerso che il classificatore Autonomy Level tendeva a sovrastimare il livello di autonomia (segnalazione di Davide Fossacecchi il 12/08: una sessione guidata strettamente dal dev veniva classificata L3 invece di L2). Il system prompt del classificatore è stato aggiornato il 17/08. Le metriche vanno quindi lette come indicazione di tendenza, non come misura assoluta: riportiamo il bias per trasparenza.

---

## 4. Come abbiamo usato OpenRouter

### 4.1 Setup dell'organizzazione
- Account organizzazione aziendale attivato il 14/07/2026; invito dei partecipanti nel canale `#prj-openrouter`.
- Workspace principale di sperimentazione: `madisoft-test`, con chiavi API dedicate per partecipante e guardrail economici settimanali per utente.
- Endpoint standardizzato compatibile con OpenAI SDK, integrato in OpenCode (con LSP abilitati), estensioni e script CLI.

### 4.2 Workspace e governance
| Workspace | Scopo | Note |
|---|---|---|
| Default Workspace | Workspace di default OpenRouter | Chiavi disattivate a fine luglio: nessun guardrail associato |
| madisoft-test | Sperimentazione team | Chiavi dedicate, guardrails settimanali, metriche classifier |

**Apprendimento chiave della governance:** i guardrail vengono ereditati dalle chiavi solo se configurati sul workspace corretto; il workspace di default va bloccato a costo zero. La configurazione di guardrail è a 3 livelli: Organization → Workspace → User, ed è più efficace impostarla a livello di workspace che di utente singolo.

### 4.3 Modelli utilizzati
| Modello | Caso d'uso prevalente | Note dal campo |
|---|---|---|
| DeepSeek V4 Flash (e 0731) | Lavoro quotidiano, planning, refactoring | Economico e produttivo; il preferito dal gruppo; "meno greedy di contesto", quindi risponde prima e costa meno |
| DeepSeek V4 Pro | Sessione lunga a basso costo | 15 centesimi per un pomeriggio di lavoro |
| GLM 5.2 | Confronto qualitativo su task complessi | Valutato al pari di modelli premium |
| Kimi 3 | Frontend, review di PR corpose | Molto forte su FE (screen/figma); episodi di interruzione a metà lavoro |
| Sonnet 4.5 | Test spot ad alta reattività | Più costoso; valutazione non favorevole per l'uso quotidiano |
| Gemini 3.5 Flash Light | Subagent in OpenCode | Richiamato di default dagli harness; da vincolare via configurazione |

> **Disponibilità in regione EU (verificata il 25/09/2026):** la lista `region=eu` di OpenRouter espone 71 modelli su 625. Del set usato in sperimentazione sono disponibili DeepSeek V4 Flash 0731, GLM 5.2 e 5.3, Kimi K2.6/K2.7, Gemini 3.5 Flash Lite e Sonnet 4.5; non è disponibile DeepSeek V4 Pro. I prezzi dei modelli del quotidiano (DeepSeek V4 Flash, Kimi, Gemini Flash Lite) restano invariati in EU.

### 4.4 Strumenti integrati
- OpenCode (harness principale, con LSP abilitati per navigazione codice e formattazione corretta).
- API OpenAI-compatible per script CLI e automazioni.
- Integrazione AI coding in Swarmia valutata come follow-up (al momento Swarmia supporta nativamente Copilot/Claude Code/Cursor, non OpenRouter; è disponibile una integrazione custom via API).

### 4.5 Periodo e partecipanti
- Canale attivo dal 14/07/2026; raccolta dati 27/07 → 26/08/2026.
- 6 sviluppatori coinvolti (D. Fossacecchi, F. Bartoli, M. Conforti, A. Jipwouo, M. Martorana, L. Piersante) con il CTO come osservatore attivo.

---

## 5. Esperimenti condotti

### 5.1 Casi d'uso reali con metriche quantitative (verificati su Jira, tutti Done)
| Issue | Caso d'uso | Metrica | Autore |
|---|---|---|---|
| [PRO-1128](https://madisoft.atlassian.net/browse/PRO-1128) | Scrittura test (con repo in-memory e builder di entità) | -60% tempi | Davide Fossacecchi |
| [PRO-1161](https://madisoft.atlassian.net/browse/PRO-1161) | Implementazione completa di test inclusi manuali | 1h vs 2-2,5h a mano | Davide Fossacecchi |
| [PRO-1187](https://madisoft.atlassian.net/browse/PRO-1187) | Test durante review; sblocco su problema tecnico reale (coda RabbitMQ creata dal consumer) | Sblocco immediato | Massimiliano Conforti |
| [PRO-1190](https://madisoft.atlassian.net/browse/PRO-1190) | PR 402 righe (con test) | 1h45m vs 4h20m della issue gemella ([PRO-1156](https://madisoft.atlassian.net/browse/PRO-1156), 319 righe); spesa 0,66€ | Davide Fossacecchi |
| [PRO-1271](https://madisoft.atlassian.net/browse/PRO-1271) | Test di 13 classi + 2 skill distillate | 1700 righe in 10h (senza AI ~ doppio) | Davide Fossacecchi |
| [PRO-1272](https://madisoft.atlassian.net/browse/PRO-1272) | Sviluppo su repository frontend mai visto prima | PR in 1h, nessun onboarding | Andrea Ercoli |
| [PRO-1249](https://madisoft.atlassian.net/browse/PRO-1249) | Trasmissione assenze SIUF Lombardia | 33% dell'epica in una giornata | Nicola Fornaciari |
| [PRO-1327](https://madisoft.atlassian.net/browse/PRO-1327) | Diagnosi fallimento test di integrazione non scritti da sé | < 3 minuti | Davide Fossacecchi |
| [PRO-1164](https://madisoft.atlassian.net/browse/PRO-1164) | Blocco eliminazione/modifica pagamenti non DA PAGARE | PR 12173 merged, +430/-68, 10 file | F. Santacroce / D. Fossacecchi |
| [PRO-1153](https://madisoft.atlassian.net/browse/PRO-1153) | Eliminazione massiva eventi solo se tutti DA PAGARE | PR 12180 +927/-4, 13 file | Davide Fossacecchi |
| [ATENA-1305](https://madisoft.atlassian.net/browse/ATENA-1305) | Feature flag salva in bozza su interpelli (frontend) | PR 77 merged 6 min dopo l'apertura, +388/-291, 15 file | Federico Bartoli |

### 5.2 Storie significative
- **[PRO-1190](https://madisoft.atlassian.net/browse/PRO-1190) (0,66€ per una PR completa):** all'agente è stato passato lo SHA del commit della issue gemella e le differenze; i test sono stati scritti autonomamente, con un refactoring in più che era comunque un miglioramento. Spesa totale 0,66€.
- **[PRO-1271](https://madisoft.atlassian.net/browse/PRO-1271) (1700 righe di test in 10h):** copertura di 13 classi fra integrazione e unitari, più 2 skill distillate per rendere più agevole il lavoro futuro e boilerplate riusabile.
- **[PRO-1272](https://madisoft.atlassian.net/browse/PRO-1272) (frontend sconosciuto in 1h):** senza onboarding, l'AI ha capito il progetto, fatto il piano e risposto ai dubbi (inclusa l'analisi del codice minificato della grid). Validato dal dev (conoscitore React): tutto corretto al primo colpo. — nota di campo: un repo con 3000 file l'AI lo ha gestito "in un soffio" dopo qualche steer, mentre Nuvola (15.000 file) richiede steering continuo.
- **Esperimento CTO (estrazione modulo Comunicazioni):** piano "a barra verde" generato in plan mode per l'estrazione del modulo. Giudizio condiviso: sensato sulla carta, da iterare punto per punto con ulteriori Plan (contestualizzato: il piano è complesso e va spezzato).
- **PR review agentica (24/08):** esperimento di apertura PR da parte dell'agente e successiva review automatica. Feedback positivo: fornisce un punto stabile in cui assegnare le revisioni. La review di PR corpose (2400 righe) con Kimi 3 ha dato risultati superiori a GLM 5.2.
- **Mob/ensemble programming con l'AI (05/08 e 26/08):** sessioni di sviluppo in coppia/ensemble usando l'AI (anche 2 issue Prometeo sviluppate senza toccare una riga di codice): l'AI ha scritto codice, commenti su Jira e PR, mentre 2 umani navigavano e verificavano i ragionamenti. Condivisa come buona pratica di trasferimento conoscenza.
- **Vibe coding (21/08):** app React completa da un PDF in 7 minuti, con giro nel browser per verifica e salto logico nel modellare il punteggio. Colore, ma indicativo del potenziale.

---

## 6. Metriche raccolte

### 6.1 Autonomy Level (classificatore, ispirato a Addy Osmani L0-L5)
| Livello | % delle richieste |
|---|---|
| L2 - Partial Autonomy (task delimitati delegati) | 58,35% |
| L3 - Conditional Autonomy (loop goal-driven) | 24,30% |
| L0 - Manual / Chat Direct | 12,85% |
| L1 - Human-Driven Assistive | 3,58% |
| L4 - High Autonomy (parallel delegation) | 0,93% |
| L5 - Full Autonomy | 0,00% |

**Lettura:** la maggioranza del lavoro è delegata all'agente su task delimitati (L2), con un quarto delle sessioni in autonomia condizionata (L3). L'uso è prevalentemente agentico (l'unico livello pienamente "assistivo", L1, è il 3,58%). Il livello L4 è marginale: la delega parallela multi-agente è ancora sperimentale.

### 6.2 Tool loop (modalità di esecuzione)
| Modalità | % delle richieste |
|---|---|
| Loop read → write → execute | 79,59% |
| Solo tool in sola lettura | 15,71% |
| Nessun tool | 4,69% |

### 6.3 Action scope (perimetro delle modifiche)
| Ambito | % delle richieste |
|---|---|
| Feature multi-file | 50,58% |
| File singolo | 32,60% |
| Intero repository | 12,72% |
| Snippet di codice | 3,50% |
| Altro / infrastruttura | 0,59% |

### 6.4 Work type (tipo di lavoro)
| Categoria | % delle richieste |
|---|---|
| Feature development | 28,96% |
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

**Lettura:** l'uso non è solo "coding generico": i primi tre tipi di lavoro (feature, refactoring, bug fixing) pesano insieme ~76%, ma c'è una quota significativa di test generation (8,23%) e research (6,63%). Conferma il potenziale "non solo per il coding" emerso anche dalla board di ideazione.

### 6.5 Costi (fonte: dashboard OpenRouter, intervallo 14/07 → 09/09/2026)
| Voce | Valore |
|---|---|
| Budget di trial disponibile | 200$ (credito aggiunto il 14/07/2026) |
| Spesa effettiva totale | **$199.76** (99,9% del budget; quasi esaurito) |
| Richieste totali | 21.849 |
| Token totali | 876M (di cui ~76,5% da cache; blended $/1M = $0,23) |
| Costo medio per sviluppatore/mese | ~$22 (≈ 6 dev × ~1,5 mesi; sotto il tetto target di 20$/dev, ma il trial è stato consumato anche dal classificatore) |
| Costi osservati nel campo | [PRO-1190](https://madisoft.atlassian.net/browse/PRO-1190): 0,66€/PR · DeepSeek V4 Flash: ~0,06$ a sessione · DeepSeek V4 Pro: 0,15$ un pomeriggio · Kimi 3: ~0,30$ |
| Incidente di governance | 40$ in 2 giorni (GPT Sol, chiave nel workspace senza guardrail) |

**Breakdown spesa per modello (fonte dashboard):**
| Modello | Spesa | Osservazioni |
|---|---|---|
| GPT-5.6 Sol | $54.81 | Il più costoso: ampia parte dovuta all'incidente di governance (auto-router scelto da un partecipante, workspace non presidiato) |
| DeepSeek V4 Pro 0423 | $40.29 | Uso quotidiano intensivo e planning |
| Kimi K3 | $35.09 | Frontend e review di PR corpose |
| Gemini 3.5 Flash Lite | $21.72 | Modello "small" per titoli/riassunti (harness e subagent) |
| DeepSeek V4 Flash 0423 | $19.27 | Uso quotidiano / refactoring (il preferito per costi) |

> Nota: la colonna "modelli più costosi per uso regolare" vs "incidente": GPT-5.6 Sol sarebbe stato evitato con una policy di routing. Il totale per modello ($171.18) non coincide con $199.76 perché il resto è attribuito al classificatore OpenRouter e ad altri consumi non riconducibili a un singolo modello. Top app per token: OpenCode (802M), OpenRouter Classifier (71M). Al 31/08 i crediti erano quasi esauriti (restavano ~3$).

---

## 7. Vantaggi e benefici osservati

Ogni vantaggio è accompagnato dall'evidenza raccolta.

- **Riduzione dei tempi sui test:** -60% su scrittura test ([PRO-1128](https://madisoft.atlassian.net/browse/PRO-1128)); 1h contro 2-2,5h manuali ([PRO-1161](https://madisoft.atlassian.net/browse/PRO-1161)); 1700 righe in 10h contro ~doppio senza AI ([PRO-1271](https://madisoft.atlassian.net/browse/PRO-1271)).
- **Velocità di consegna:** PR 402 righe in 1h45m contro 4h20m della gemella ([PRO-1190](https://madisoft.atlassian.net/browse/PRO-1190)); PR 77 merged 6 minuti dopo l'apertura ([ATENA-1305](https://madisoft.atlassian.net/browse/ATENA-1305)); 33% dell'epica in una giornata ([PRO-1249](https://madisoft.atlassian.net/browse/PRO-1249)).
- **Diagnostica rapida:** causa di test di integrazione falliti individuata in 3 minuti ([PRO-1327](https://madisoft.atlassian.net/browse/PRO-1327)); sblocco su problema reale RabbitMQ durante review ([PRO-1187](https://madisoft.atlassian.net/browse/PRO-1187)).
- **Onboarding azzerato su codebase ignote:** repo frontend mai visto, PR in 1h con piano e analisi di codice minificato ([PRO-1272](https://madisoft.atlassian.net/browse/PRO-1272)).
- **Costo per task competitivo:** 0,66€ per una PR completa ([PRO-1190](https://madisoft.atlassian.net/browse/PRO-1190)); modelli economici di alta qualità (DeepSeek V4 Flash/Pro).
- **Flessibilità assoluta:** cambio istantaneo di modello per task (scelta del modello giusto al momento giusto, no lock-in).
- **Governance e visibilità:** dashboard per workspace, guardrail economici, chiavi dedicate, classificatori per metriche di utilizzo.
- **Crescita di skill collettiva:** 2 skill distillate per il lavoro futuro ([PRO-1271](https://madisoft.atlassian.net/browse/PRO-1271)), momenti di mob programming con l'AI, e un modello di conoscenza condivisibile (prompt/skill come "nuovo codice sorgente").

---

## 8. Voci dal campo

Citazioni selezionate dal canale `#prj-openrouter` (14/07 → 26/08/2026).

### Professionali
> "Io uso parecchio Copilot per le sole review, perché per tutti gli altri utilizzi dura troppo poco." — Lorenzo Piersante

> "Il logging è un obbligo, non un'opzione. Come soggetto NIS2 essenziale dobbiamo garantire la tracciabilità delle operazioni." — Pasquale Siciliano (IT-Security)

> "Secondo me il classificatore sul livello di autonomia che abbiamo creato è troppo ottimistico." — Davide Fossacecchi

> "Sto gruppo di test e queste conversazioni sono per me Food for Thought." — Francesco Trucchia (CTO)

> "Per me DS4 Flash rimane il coltellino svizzero." — Davide Fossacecchi

> "Dovremmo avere AI Champion di team e una Cop AI." — Davide Fossacecchi

### Momenti di colore
> "Ho fatto una roba con Sonnet 4.5... NON L'AVESSI MAI FATTO. Ci pagavo Kimi con quei soldi e mi davano anche il resto." — Davide Fossacecchi

> "mi sa che c'è un bug sul prezzo del budget: vedo 6 euro al posto di 600 euro" — Massimiliano Conforti (il guardrail economico mostrava 6€)

> "vai a casa umano" — Kimi 3 (riportato da Federico Bartoli)

> "Si sboccia! 🍾" — Ferdinando Santacroce (sull'incidente dei 40$ in 2 giorni)

---

## 9. Limiti e criticità evidenziati

- **Guardrails legati al workspace, non alle chiavi:** una chiave creata nel workspace sbagliato bypassa i guardrail economici. Incidente reale: 40$ spesi in 2 giorni con GPT Sol (auto-router) da un partecipante. Mitigato bloccando a zero il workspace di default.
- **Auto-router da usare con cautela:** il routing automatico ha selezionato GPT Sol, modello costoso. Da limitare o configurare con policy (white-list/black-list dei modelli) o con il suffisso `:floor`.
- **Classificatore Autonomy Level ottimistico:** tendeva a sopravvalutare l'autonomia (L3 vs L2 reale); aggiornato il 17/08.
- **Qualità non omogenea dei provider:** per lo stesso modello la reattività varia a seconda del provider; episodi di degradazione percepita (DeepSeek V4 Flash "degradato" il 03/08; token/s variabili da 6 a 30).
- **Stabilità dei modelli nuovi:** Kimi 3 ha mostrato episodi di interruzione a metà lavoro con consumo di credito.
- **Catalogo EU più ristretto (gestito):** in regione EU sono disponibili 71 modelli su 625 (~11%). Ci sono i modelli usati nel quotidiano (DeepSeek V4 Flash 0731, GLM 5.2/5.3, Kimi K2.6/K2.7, Gemini 3.5 Flash Lite, Sonnet 4.5); non è disponibile DeepSeek V4 Pro. Il routing esclusivo EU è attivabile con il passaggio al piano Business.
- **Integrazione con GitHub/Swarmia assente:** la review direttamente su GitHub (come Copilot) non è nativa; Swarmia non espone integrazione per OpenRouter (da costruire via API custom).
- **Repo di grandi dimensioni:** su Nuvola (15.000 file) l'incidenza del contesto è significativa e pesa sui consumi; il costo del classificatore può superare il costo del modello selezionato.
- **Tema aperto su I/O logging e NIS2:** obbligo di tracciabilità (IT-Security) vs rischi di privacy/alterazione del comportamento (team). Decisione da formalizzare; l'endpoint EU attualmente non supporta il logging (risolto a monte).

---

## 10. Confronto con GitHub Copilot (fornitore attuale)

### 10.1 Tabella comparativa
| Criterio | GitHub Copilot | OpenRouter | Note / Evidenze |
|---|---|---|---|
| Modelli disponibili | Predefiniti, chiusi | 400+ (Open Weights di frontiera inclusi) | DeepSeek, GLM, Kimi testati in produzione |
| Pricing | Abbonamento a consumo che si esaurisce | Pay-as-you-go, spesa proporzionata all'uso reale | [PRO-1190](https://madisoft.atlassian.net/browse/PRO-1190): 0,66€/PR |
| Durata abbonamento | Budget mensile si esaurisce in poche ore | Uso elastico senza tetto rigido | Confermato nel canale ("per tutti gli altri utilizzi dura troppo poco") |
| Flessibilità del modello | Bloccato | Intercambiabilità istantanea | Modello scelto per task |
| Controllo costi | Scarsa visibilità | Workspace, budget policy, guardrails con blocchi automatici | Incidente 40$ → guardrails |
| Back-office / governance | Ambiente utente chiuso | Console completa: seats, cap, guardrail, classificatori | Requisito MoSCoW M |
| Review su GitHub | Nativa | Non nativa (si replica con agenti/action custom) | Gap noto |
| Data residency / compliance | [DA INSERIRE] | EU API + ZDR contrattuale (DPA); 71 modelli in regione EU | [IS-313](https://madisoft.atlassian.net/browse/IS-313) compliant |

### 10.2 Evidenza del problema principale
Il difetto più rilevante di GitHub Copilot per Madisoft è la durata dell'abbonamento: un programmatore medio esaurisce il plafond in poche ore di lavoro agentico, contro la settimana o il mese previsti da contratto. Questo si traduce in stop forzati a metà giornata e nel razionamento dell'uso (come testimoniato nel canale, dove Copilot resta utile solo per le review). Il confronto quantitativo è reso evidente dal caso [PRO-1190](https://madisoft.atlassian.net/browse/PRO-1190) vs la sua gemella [PRO-1156](https://madisoft.atlassian.net/browse/PRO-1156) (stessa tipologia di issue, test generati con Copilot): con OpenRouter una PR completa da 402 righe è costata 0,66€ in 1h45m.

> Dato numerico puntuale sulla durata dell'abbonamento Copilot: [DA INSERIRE].   
> Evidenze qualitative: il CTO indica il costo attuale a 20€/dev/mese; l'epica Copilot [NUV-18452](https://madisoft.atlassian.net/browse/NUV-18452) (Done) testimonia la sperimentazione precedente. 

---

## 11. Cosa abbiamo imparato su OpenRouter

| Lezione | Impatto concreto |
|---|---|
| Guardrails a zero sul workspace di default | Previene lo sforamento incontrollato (incidente 40$ con GPT Sol) |
| Workspace = team | Dashboard di utilizzo per team con log per team (requisito CTO: "l'unità minima è il team") |
| Chiavi API dedicate per utente/workspace | Isolamento ambienti e attribuzione dei consumi |
| Auto-router con policy | Evita la selezione di modelli costosi (GPT Sol); meglio white-list o `:floor` |
| `:floor` per il routing sul provider più economico | Abbattimento dinamico dei costi rispetto ai prezzi fissi dei competitor |
| Scelta del modello per task | DeepSeek V4 Flash per il quotidiano, Kimi 3 per FE/review corpose, GLM 5.2 per confronti complessi |
| Classificatori per metriche di utilizzo | Misurazione del tipo di utilizzo senza esporre i prompt (privacy) |
| Preferire modelli economici e produttivi | DeepSeek V4 Flash 0731 "ancora più economico e produttivo"; Sonnet 4.5 non conveniente per l'uso quotidiano |
| Configurare lo small_model | Evita consumi inattesi (Nano Banana 2/Gemini per titoli di sessione in OpenCode) |

---

## 12. Sicurezza & Compliance

### 12.1 Stato
- **[IS-313](https://madisoft.atlassian.net/browse/IS-313)** — Valutazione sicurezza OpenRouter Enterprise: **Done** (Pasquale Siciliano).
- **Qualifica Fornitore e DPIA - OpenRouter Enterprise** (codice PG-PUR-01/OR-2026, rev. 1.0, 05/08/2026, space TIS, page 528023559): **approvata, stato Green**.
- **Esito:** compliant (con riserva) per l'utilizzo dello strumento. La riserva riguarda l'attivazione del routing esclusivo EU, ora disponibile con il passaggio al piano Business (vedi 12.3).

### 12.2 Direttive obbligatorie (da applicare a monte)
1. **Data Residency:** configurare esclusivamente le regioni EU per l'elaborazione dei dati, passando al piano Business e attivando il routing EU.
2. **Prevenzione leak:** `.cbmignore` / `.gitignore` per escludere file `.env`, chiavi SSH, certificati e dati personali dal transito verso l'IA.
3. **Zero Data Retention:** selezionare esclusivamente i modelli che supportano la ZDR contrattuale.

### 12.3 Stato di avanzamento e temi aperti
- **ZDR:** già operativo.
- **Routing esclusivo EU:** disponibile con il passaggio al piano Business (indicazione di OpenRouter del 25/09/2026). In regione EU sono pubblicati 71 modelli su 625 (~11%): presenti DeepSeek V4 Flash 0731, GLM 5.2/5.3, Kimi K2.6/K2.7, Gemini 3.5 Flash Lite e Sonnet 4.5; non disponibile DeepSeek V4 Pro. Il vincolo "solo modelli EU" non rende inutilizzabile il setup: i modelli del quotidiano ci sono. Elenco aggiornato: [openrouter.ai/models?region=eu](https://openrouter.ai/models?region=eu). Routing EU-only e ZDR confermati (riunione del 12/10/2026); il piano Business si sottoscrive con tali garanzie.
- **I/O logging:** al momento non applicabile all'endpoint EU (risolto a monte). Dibattito aperto su logging e monitoraggio: obbligo di tracciabilità NIS2 (IT-Security) vs rischi di privacy e di alterazione del comportamento (team). Decisione da formalizzare. Possibilità di inviare log esternamente (AWS/SIEM) da valutare quando disponibile per l'EU.
- **Sandboxing degli agenti:** valutazione futura per isolare l'esecuzione degli agenti dal file system locale.

---

## 13. Piano di adozione (approvato)

### 13.1 Fasi
Approvato in riunione il 12/10/2026 da CTO e CEO. Il primo passo è il passaggio al piano Business di OpenRouter: Ferdinando Santacroce e Pasquale Siciliano contattano OpenRouter, ottengono conferma scritta che il piano includa il routing esclusivo EU e la Zero Data Retention contrattuale, e, una volta confermato anche da Pasquale (referente cybersecurity), si procede alla sottoscrizione con il supporto del CEO (Diego Moretti). Da quel momento parte l'implementazione descritta di seguito; l'avvio operativo inizia con il kickoff del 13/10/2026.

| Fase | Attività | Timeline | Responsabile |
|---|---|---|---|
| 1 | **Passaggio al piano Business di OpenRouter** (conferma scritta di routing EU-only e ZDR, verifica IT-Security, sottoscrizione con CEO) | Subito dopo l'approvazione | F. Santacroce + P. Siciliano + D. Moretti (CEO) |
| 2 | Kickoff, comunicazione e aggiornamento guardrails (default workspace a zero, workspace per team) | Ottobre 2026 | F. Santacroce |
| 3 | Onboarding degli sviluppatori (chiavi dedicate, tooling OpenCode, policy modello) | Ottobre 2026 | F. Santacroce |
| 4 | Spostamento del budget ricorrente 20$/mese/dev da Copilot verso OpenRouter | Da rollout | F. Santacroce |
| 5 | Attivazione routing EU esclusivo (piano Business) e verifica compliance ZDR/DPIA | Al rollout | F. Santacroce + IT-Security |
| 6 | Configurazione integrazione metriche (Swarmia custom / dashboard per team) | Novembre 2026 | Team + CTO |
| 7 | Monitoraggio consumi e checkpoint mensile (metriche classifier + costi) | Continuo | F. Santacroce |

### 13.2 Budget richiesto
- Costo di avvio: già sostenuto (trial 200$; spesa effettiva a fine sperimentazione: **$199.76** su $200).
- Costo ricorrente: target **≤ 20$/mese/dev** (come da SSR); spesa media osservata in sperimentazione ~22$/dev/mese a causa del consumo del classificatore e dell'incidente GPT-5.6 Sol. Con una policy di routing e guardrails corretti, la proiezione è di mantener/e scendere sotto il target.

### 13.3 Metriche di successo post-adozione
- Mantenimento della spesa ≤ 20$/mese/dev.
- Riduzione dei tempi sui task di refactoring (target -20%, con riduzioni già osservate fino al 60% sui test).
- Conformità EU/ZDR al 100%.
- Soddisfazione sviluppatori (survey a 90 giorni).
- Adozione per team visibile su dashboard (workspace per team).

### 13.4 Rischi residui e mitigazioni
| Rischio | Mitigazione |
|---|---|
| Sforamenti di spesa per configurazioni errate | Guardrails a zero sul default workspace; verifica ereditarietà chiavi |
| Selezione modelli costosi via auto-router | Policy/white-list modelli, uso di `:floor` |
| Disomogeneità provider sullo stesso modello | Test di reattività prima dell'adozione a livello di team |
| Limiti modelli EU | Attivazione routing EU (piano Business); 71 modelli disponibili, monitoraggio listino EU |
| Conformità logging (NIS2 vs privacy) | Decisione formale condivisa con IT-Security/HR |

---

## 14. Approvazione

Esito: il piano di adozione descritto in sezione 13, il passaggio al piano Business di OpenRouter e il budget associato sono stati **approvati in riunione il 12/10/2026** da CTO (Francesco Trucchia) e CEO (Diego Moretti), con spostamento del budget ricorrente da GitHub Copilot verso OpenRouter. Non è prevista una firma formale: l'approvazione è stata data in sede di meeting e il CEO ha caricato il budget sul conto OpenRouter.

| Ruolo | Nome | Decisione | Data |
|---|---|---|---|
| Owner | Ferdinando Santacroce | Proponente | 25/09/2026 |
| CTO | Francesco Trucchia | Approvato | 12/10/2026 |
| CEO | Diego Moretti | Approvato (budget caricato) | 12/10/2026 |
| IT & CyberSecurity | Pasquale Siciliano | Routing EU-only e ZDR confermati | 12/10/2026 |

---

## 15. Riferimenti

- Pitch: adozione OpenRouter
- SSR: adozione OpenRouter
- Offerta OpenRouter per Madisoft
- DPA OpenRouter (EU Processing Commitments)
- [IS-313](https://madisoft.atlassian.net/browse/IS-313) — Valutazione sicurezza OpenRouter Enterprise
- Qualifica Fornitore e DPIA - OpenRouter Enterprise — Confluence (TIS, https://madisoft.atlassian.net/wiki/spaces/TIS/pages/528023559/…)
- Engineering Tech Strategy 2026–2028 — Confluence (PI, https://madisoft.atlassian.net/wiki/spaces/PI/pages/36274209/…)
- Spazio Confluence **Verso Nuvola3** (VN3) — iniziative di disaccoppiamento (https://madisoft.atlassian.net/wiki/spaces/VN3)
- OpenRouter Documentation Portal
- Modelli disponibili in regione EU (verificati il 25/09/2026): https://openrouter.ai/models?region=eu
- Canale Slack `#prj-openrouter` (14/07 → 26/08/2026)
- Epica Jira: **[STAFF-118](https://madisoft.atlassian.net/browse/STAFF-118)** "OpenRouter: adozione come AI gateway aziendale"
- Iniziativa Swarmia: [DA INSERIRE: link Swarmia]
- Board Miro (workshop di ideazione) · classificatori configurati (L0-L5 Autonomy, Engineering Work)
- Metriche classifier: vedi Appendice B (valori grezzi)

---

## Tracciamento Jira

Le attività dell'iniziativa OpenRouter sono tracciate nel progetto **STAFF** (Team Staff+):

- [STAFF-118](https://madisoft.atlassian.net/browse/STAFF-118) - OpenRouter: adozione come AI gateway aziendale (Epica contenitore).
- [STAFF-119](https://madisoft.atlassian.net/browse/STAFF-119) - ricerca informazioni e materiale di valutazione.
- [STAFF-120](https://madisoft.atlassian.net/browse/STAFF-120) - creazione del pitch di adozione.
- [STAFF-121](https://madisoft.atlassian.net/browse/STAFF-121) - presentazione del pitch a CEO e CTO.
- [STAFF-122](https://madisoft.atlassian.net/browse/STAFF-122) - sperimentazione con il gruppo di sviluppo.
- [STAFF-105](https://madisoft.atlassian.net/browse/STAFF-105) - redazione del report finale di sperimentazione (questo documento).
- [STAFF-123](https://madisoft.atlassian.net/browse/STAFF-123) - approvazione del piano di adozione.
- [STAFF-124](https://madisoft.atlassian.net/browse/STAFF-124) - piano di rollout.
- [STAFF-125](https://madisoft.atlassian.net/browse/STAFF-125) - linea guida server MCP locali e richiesta [IS-395](https://madisoft.atlassian.net/browse/IS-395).

---

## Appendice A — Mappa partecipanti
| Persona | Ruolo/Team | Ruolo nella sperimentazione |
|---|---|---|
| Ferdinando Santacroce | [AMET] Staff Engineer | Owner, setup, metriche |
| Davide Fossacecchi | Dev backend | Utilizzo intensivo, casi [PRO-1128](https://madisoft.atlassian.net/browse/PRO-1128)/1161/1190/1271/1327/1153 |
| Federico Bartoli | [Atena] Frontend dev | Utilizzo frontend, [ATENA-1305](https://madisoft.atlassian.net/browse/ATENA-1305) (PR 77) |
| Massimiliano Conforti | Dev | [PRO-1187](https://madisoft.atlassian.net/browse/PRO-1187), valutazioni modelli |
| Marco Martorana | Dev | Incidente guardrails 40$ (lezione appresa) |
| Lorenzo Piersante | [Atena] Backend dev | Confronto Copilot (review), considerazioni privacy |
| Anders Jipwouo | Dev | Utilizzo e confronto flussi |
| Francesco Trucchia | CTO | Requisiti metriche, esperimento Comunicazioni, decisione |
| Pasquale Siciliano | IT-Security | [IS-313](https://madisoft.atlassian.net/browse/IS-313), direttive compliance |

## Appendice B — Dettaglio metriche classifier (valori grezzi)

### Autonomy Level
| Livello | Value | % |
|---|---|---|
| L2_Partial | 24.231919 | 58.35 |
| L3_Conditional | 10.090247 | 24.30 |
| L0_Manual | 5.336758 | 12.85 |
| L1_Assistive | 1.485288 | 3.58 |
| L4_High | 0.386986 | 0.93 |

### Tool Loop
| Modalità | Value | % |
|---|---|---|
| read_write_execute_loop | 33.056226 | 79.59 |
| read_only_tools | 6.526626 | 15.71 |
| no_tools | 1.948346 | 4.69 |

### Action Scope
| Ambito | Value | % |
|---|---|---|
| multi_file_feature | 21.007974 | 50.58 |
| single_file | 13.539399 | 32.60 |
| entire_repository | 5.283542 | 12.72 |
| snippet_code | 1.452966 | 3.50 |
| Other | 0.241332 | 0.58 |
| system_infrastructure | 0.005985 | 0.01 |

### Work Type
| Categoria | Value | % |
|---|---|---|
| Feature development | 12.099488 | 28.96 |
| Refactoring | 10.122866 | 24.23 |
| Bug fixing | 9.480858 | 22.69 |
| Unit test generation | 3.439004 | 8.23 |
| Research & exploration | 2.769786 | 6.63 |
| Code quality | 2.19802 | 5.26 |
| Documentazione | 0.486754 | 1.17 |
| Migrations & upgrades | 0.377261 | 0.90 |
| CI/CD & DevOps | 0.334493 | 0.80 |
| Code review | 0.280356 | 0.67 |
| Other | 0.154824 | 0.37 |
| Security | 0.027821 | 0.07 |
| Data & automation | 0.00939 | 0.02 |

## Appendice C — Modelli disponibili in regione EU

Fonte: [openrouter.ai/models?region=eu](https://openrouter.ai/models?region=eu) (endpoint pubblico `GET /api/frontend/v1/models/find?active=true&fmt=cards&region=eu`), verifica del 25/09/2026. **71 voci restituite su 625 totali (~11%); 70 modelli distinti** (`google/gemini-2.5-flash-lite` compare duplicato nella risposta).

✅ = modello usato nella sperimentazione · ❌ = usato ma non disponibile in EU.

| Autore | Modelli in regione EU |
|---|---|
| OpenAI (22) | gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, gpt-4o-mini, gpt-5, gpt-5.1, gpt-5.4, gpt-5.5, gpt-5.6-luna, gpt-5.6-luna-pro, gpt-5.6-sol, gpt-5.6-sol-pro, gpt-5.6-terra, gpt-5.6-terra-pro, gpt-5-mini, gpt-5-nano, gpt-6-luna, gpt-6-luna-pro, gpt-6-sol, gpt-6-sol-pro, gpt-oss-120b, gpt-oss-20b |
| Mistral AI (21) | codestral-2508, codestral-embed-2505, devstral-2512, ministral-14b-2512, ministral-3b-2512, ministral-8b-2512, mistral-embed-2312, mistral-large, mistral-large-2407, mistral-large-2512, mistral-medium-3, mistral-medium-3.1, mistral-medium-3-5, mistral-nemo, mistral-saba, mistral-small-2603, mistral-small-3.2-24b-instruct, mixtral-8x22b-instruct, voxtral-mini-transcribe, voxtral-mini-tts-2603, voxtral-small-24b-2507 |
| Anthropic (12) | claude-fable-5, claude-haiku-4.5, claude-opus-4.5, claude-opus-4.6, claude-opus-4.7, claude-opus-4.8, claude-opus-5, claude-opus-5.5, claude-sonnet-4, ✅ claude-sonnet-4.5, claude-sonnet-4.6, claude-sonnet-5 |
| Google (6, con `gemini-2.5-flash-lite` duplicato) | gemini-2.5-flash, gemini-2.5-flash-lite, gemini-2.5-pro, gemini-3.1-flash-lite, ✅ gemini-3.5-flash-lite, gemini-embedding-2 |
| Amazon (4) | nova-2-lite-v1, nova-lite-v1, nova-micro-v1, nova-pro-v1 |
| Z.ai (2) | ✅ glm-5.2, glm-5.3 |
| Moonshot (2) | ✅ kimi-k2.6, ✅ kimi-k2.7-code |
| DeepSeek (1) | ✅ deepseek-v4-flash-0731 |

**Modelli usati ma NON disponibili in regione EU:** ❌ `deepseek/deepseek-v4-pro` (secondo modello per spesa, $40.29).
