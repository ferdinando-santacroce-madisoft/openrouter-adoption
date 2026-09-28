# Piano di rollout: adozione OpenRouter

## Scheda documento

| Campo | Valore |
| :---- | :---- |
| Titolo | Piano di rollout: adozione OpenRouter |
| Versione | 0.1 (bozza) |
| Data | 25/09/2026 |
| Autore / Owner | Ferdinando Santacroce |
| Destinatari | Diego Moretti (CEO), Francesco Trucchia (CTO), Pasquale Siciliano (IT & Security), team di sviluppo |
| Stato | BOZZA: ossatura da completare |
| Classificazione | Riservato: uso interno |
| Documenti correlati | [SSR - OpenRouter](ssr-adozione-openrouter.md), [Report finale: sperimentazione OpenRouter](report-finale-openrouter.md), [Pitch: adozione OpenRouter](pitch-adozione-openrouter.md) |

## Cronologia revisioni

| Versione | Data | Autore | Descrizione |
| :---- | :---- | :---- | :---- |
| 0.1 | 25/09/2026 | Ferdinando Santacroce | Prima ossatura del piano: capitoli, stima di budget e marcatori sui punti da esplorare. |

## 1. Scopo del documento

Dopo la sperimentazione e la decisione di proseguire, questo documento definisce il piano operativo per introdurre OpenRouter in azienda. Non ripete la valutazione tecnica e di sicurezza, già coperta da SSR e Report finale, ma ne traduce le conclusioni in azioni: budget, configurazione della piattaforma, roll out e formazione, misurazione dell'impatto.

Il piano copre sia la parte economica e di indirizzo sia la parte esecutiva. Dove serve una conferma esplicita, il punto è marcato con un richiamo all'attenzione del soggetto competente.

### 1.1 Orizzonte temporale

L'obiettivo è avere OpenRouter disponibile per tutti **entro fine ottobre 2026**.

### 1.2 Criteri di uscita (exit criteria)

Il rollout si considera completato quando sono soddisfatti tutti i punti seguenti:

- [ ] Ogni sviluppatore ha un accesso a OpenRouter.
- [ ] Ogni team ha il proprio workspace dedicato con i relativi guardrail di spesa.
- [ ] Ogni sviluppatore ha accesso al solo workspace del proprio team.
- [ ] Ogni team ha un **AI Champion** definito: una persona di riferimento per l'intelligenza artificiale in generale e per OpenRouter in particolare, che sa raccogliere le necessità, dare supporto e fare da primo livello di interazione sugli strumenti AI.
- [ ] Ogni sviluppatore ha confermato di riuscire a usare gli strumenti di intelligenza artificiale nel proprio workflow quotidiano: in VS Code, in PhpStorm, nelle applicazioni CLI o in altre harness.
- [ ] Il guardrail globale di spesa è impostato per non superare la spesa mensile prefissata; è stata decisa la modalità dei guardrail (per persona o per team).

## 2. Budget e sostenibilità economica

### 2.1 Stato attuale: GitHub Copilot

- Costo attuale: **20 $/mese per persona**.
- Popolazione assunta: **25 persone**.
- Costo ricorrente: 25 x 20 $ = **500 $/mese**, pari a **6.000 $/anno**.

### 2.2 Come funziona il costo di OpenRouter

OpenRouter non ha un abbonamento per persona. Il modello è diverso da Copilot:

- Si **caricano crediti** una volta (pagamento anticipato) e i crediti vengono consumati in base all'uso reale (pay-as-you-go).
- La stessa ricarica può essere **ripartita a piacere** tra gli utilizzatori, tramite workspace e chiavi API dedicate.
- È prevista una **fee di piattaforma del 5,5%** sul momento della ricarica dei crediti.
- Il costo dipende dal modello scelto e dal routing (con l'istruzione `:floor` si può puntare al fornitore momentaneamente più economico).

Conseguenza pratica: la richiesta non è una licenza a testa, ma una **ricarica di credito** con cui coprire l'equivalente del budget attuale.

### 2.3 Fabbisogno per il 2026 (ottobre-dicembre)

Per semplicità si considerano i tre mesi che restano da qui a fine 2026: ottobre, novembre e dicembre.

| Voce | Calcolo | Valore |
| :---- | :---- | :---- |
| Inferenza equivalente | 25 dev x 20 $ x 3 mesi | 1.500 $ |
| Fee di ricarica 5,5% | 1.500 $ x 5,5% | 82,50 $ |
| **Ricarica consigliata 2026** | arrotondamento | **~1.600 $** |

### 2.4 Stima per il 2027

| Voce | Calcolo | Valore |
| :---- | :---- | :---- |
| Inferenza equivalente | 25 dev x 20 $ x 12 mesi | 6.000 $ |
| Fee di ricarica 5,5% | 6.000 $ x 5,5% | 330 $ |
| **Ricarica consigliata 2027** | arrotondamento | **~6.350 $** |

### 2.5 Sintesi della richiesta

| Periodo | Copilot (status quo) | OpenRouter (equivalente + fee) |
| :---- | :---- | :---- |
| Ottobre-dicembre 2026 | 1.500 $ | ~1.600 $ |
| Anno 2027 | 6.000 $ | ~6.350 $ |

L'iniziativa è **sostanzialmente neutra**: non aggiunge un costo nuovo, ma **sposta** il budget ricorrente oggi allocato su Copilot verso OpenRouter. L'unica differenza è la fee di ricarica del 5,5% e l'eventuale periodo di sovrapposizione dei due strumenti.

> **DA CONFERMARE con Diego**: la ricarica di ~1.600 $ per ottobre-dicembre 2026 e la stima di ~6.350 $ per il 2027.

### 2.6 Ipotesi e variabili da verificare

> **DA DECIDERE**: 25 persone sono la popolazione target del rollout o solo il perimetro iniziale? Vista la natura del servizio, possiamo aggiungere e togliere persone quando vogliamo, ricalibrando il budget possibilmente.
> **DA DECIDERE**: se mantenere Copilot in parallelo durante la transizione e per quanto (direi di tenerlo fino a fine anno).
> **DA VERIFICARE**: fatturazione (modalità, valuta, etc.).

## 3. Piano di configurazione di OpenRouter

### 3.1 Organizzazione e Workspaces

Ipotesi di partenza: un **workspace per team** (prodotto, platform, IT&Security, Staff+).

> **DA DECIDERE**: numero e mappa dei workspace; naming convention; chi amministra i workspace (il "superadmin" di turno); come gestire account di persone che non fanno parte di un team (ad es. account di Francesco T. e Diego, eventuali account per designer, etc.).

### 3.2 Guardrails e budget policies

I guardrails di OpenRouter operano su tre livelli: Organization, Workspace, User.

Opzioni sul tavolo:

- cap **per persona** (20 $/mese), coerente con il budget Copilot;
- cap **per team** (una cifra aggregata, con elasticità interna al team);
- **mix** dei due: tetto di team come limite di sicurezza e tetto per persona come indirizzo.

### 3.3 Data residency: modelli europei e routing

Vincolo di conformità: **bloccare i modelli non europei** e mantenere il routing esclusivamente in EU/EEA, con Zero Data Retention contrattuale (piano Business).

- Elenco aggiornato dei modelli disponibili in regione EU: https://openrouter.ai/models?region=eu
- Al 25/09/2026 risultano 71 modelli su 625 (~11%): presenti DeepSeek V4 Flash, GLM 5.2/5.3, Kimi K2.6/K2.7, Gemini 3.5 Flash Lite, Sonnet 4.5.

> **DA CONFERMARE con Pasquale**: conferma che il piano Business sia impostato con routing EU-only e Zero Data Retention contrattuale, prima della sottoscrizione.

### 3.4 Classifier e osservabilità

La sperimentazione ha usato i classificatori di OpenRouter per taggare le generazioni (non i prompt) e aggregare metriche:

| Classificatore | Scopo | Ispirazione |
| :---- | :---- | :---- |
| Autonomy Level | Livello di autonomia agentica, da L0 a L5 | Framework di Addy Osmani |
| Engineering Work | Categoria di lavoro ingegneristico | Tassonomia interna |

> **DA ESPLORARE**: nuovi classificatori, necessità di dashboard e aggregazioni per workspace; metriche ed eventuale reportistica.

### 3.5 Chiavi API, BYOK e sicurezza

> **DA ESPLORARE**: ciclo di vita delle chiavi API (creazione, assegnazione, rotazione, revoca); disabilitare Bring Your Own Key (non permettiamo che qualcuno aggiunga e usi provider terzi non aziendali); logging e tracciabilità NIS2.

## 4. Piano di roll out e formazione

### 4.1 Fasi e timeline

| Fase | Attività | Timeline | Responsabile |
| :---- | :---- | :---- | :---- |
| 1 | Passaggio al piano Business e conferma scritta di routing EU-only e ZDR | Subito dopo l'approvazione | F. Santacroce + P. Siciliano |
| 2 | Kickoff, comunicazione e configurazione guardrails e workspace | Ottobre 2026 | F. Santacroce |
| 3 | Onboarding dei team e distribuzione chiavi | Ottobre 2026 | F. Santacroce + AI Champion |
| 4 | Formazione iniziale e materiali how-to | Ottobre 2026 | F. Santacroce + AI Champion |
| 5 | Spostamento del budget ricorrente da Copilot a OpenRouter | Al rollout | F. Santacroce + Diego Moretti |
| 6 | Monitoraggio consumi e checkpoint periodici | Continuo | F. Santacroce + Francesco Trucchia |

> **DA APPROFONDIRE**: ordine di onboarding dei team, dipendenze e criteri di ingresso per ciascuna fase (i criteri di uscita del rollout sono in 1.2).
> **Con Diego**: sottoscrizione del piano Business e approvazione del budget associato.

### 4.2 Integrazione con gli strumenti di sviluppo

I percorsi di adozione da coprire con guide dedicate:

| Percorso | Descrizione | Stato |
| :---- | :---- | :---- |
| A | PhpStorm con plugin GitHub Copilot configurato con OpenRouter come provider | DA ESPLORARE |
| B | VS Code con plugin GitHub Copilot configurato con OpenRouter | DA ESPLORARE |
| C | OpenRouter come provider diretto nell'IDE, senza passare dal plugin Copilot | DA ESPLORARE |
| D | OpenRouter con CLI e agente a scelta (es. opencode) | DA ESPLORARE |

> **DA PRODURRE**: per ogni percorso servono ricerca, piccolo manuale how-to e prova pratica (screenshot, passaggi, limiti noti). I materiali alimenteranno la formazione iniziale.

### 4.3 Formazione iniziale

Obiettivo: mettere in grado di usare lo strumento partendo dagli strumenti che i dev usano già (IDE e plugin esistenti).

> **DA APPROFONDIRE**: contenuti e durata; target e prerequisiti; formato (demo, workshop); materiali di riferimento aggiornati.

### 4.4 Programma AI Champion per team

Per ogni team va individuato un **AI Champion**: una persona di riferimento per le questioni sull'intelligenza artificiale in generale e su OpenRouter in particolare. Sa raccogliere le necessità dei colleghi, dà supporto e costituisce il primo livello di interazione e di supporto sugli strumenti AI. Fa anche da referente del feedback verso l'owner dell'iniziativa.

Rete di supporto di secondo livello: Nando e i partecipanti alla gilda sull'intelligenza artificiale.

> **DA DECIDERE**: criteri di selezione dell'AI Champion; come si riconosce il ruolo; carico atteso; canale di comunicazione (es. canale Slack dedicato); come si raccolgono i problemi ricorrenti per trasformarli in FAQ e guide.

### 4.5 Comunicazione e gestione del cambiamento

> **DA APPROFONDIRE**: piano di comunicazione (perché cambiamo, cosa cambia per i dev, cosa resta), gestione delle aspettative e dei casi d'uso, gestione del doppio strumento durante la transizione.

## 5. Misurazione di adozione e impatto

### 5.1 Metriche di adozione

- Utilizzatori attivi per team e per workspace.
- Chiavi attive e consumi per modello e per caso d'uso.
- Distribuzione dei livelli di autonomia (classifier) e dei tipi di lavoro.

### 5.2 Metriche di impatto sulla produttività

> **DA ESPLORARE**: quali indicatori usare e con quale cadenza, per valutare se lo strumento ha un impatto positivo, neutro o negativo. Piste da valutare: lead time e throughput delle PR, tempo su refactoring e test, spesa per PR, qualità (difetti), affiancamento a pratiche di pair/mob programming. Le metriche aggregate per team sono il livello di lettura preferito.

### 5.3 Strumenti e fonti

- Dashboard OpenRouter per workspace (consumi e modelli).
- Classificatori OpenRouter (autonomia, tipo di lavoro).
- Jira e GitHub per throughput e lead time.
- Swarmia (integrazione custom da valutare).
- Survey periodica di soddisfazione.

### 5.4 Cadenza dei checkpoint

> **DA DECIDERE**: frequenza dei checkpoint (mensile magari all'inizio, poi trimestrale), chi analizza i dati, a chi vengono riportati e quali soglie fanno scattare correzioni.

## 6. Rischi e mitigazioni

| Rischio | Mitigazione |
| :---- | :---- |
| Sforamenti di spesa per configurazioni errate | Default workspace a zero; verifica ereditarietà chiavi; cap per team e per persona |
| Selezione di modelli costosi via auto-router | White-list modelli e uso di `:floor` |
| Disomogeneità dei provider sullo stesso modello | Test di reattività prima dell'adozione per team |
| Logging e tracciabilità (NIS2) contro rischi di privacy | Decisione formale condivisa con Pasquale |
| Sovrapposizione Copilot e OpenRouter durante la transizione | Finestra di overlap breve e pianificata |
| Adozione disomogenea tra i team | AI Champion per team e guide how-to dedicate |

## 7. Ruoli e responsabilità

| Ruolo | Persona | Responsabilità |
| :---- | :---- | :---- |
| Owner dell'iniziativa | Ferdinando Santacroce | Piano, budget, configurazione, coordinamento |
| Sponsor tecnico | Francesco Trucchia (CTO) | Indirizzo, coerenza con la Tech Strategy, metriche |
| Approvatore budget | Diego Moretti (CEO) | Budget di spesa preventivata |
| IT & Security | Pasquale Siciliano | Conformità EU/ZDR, sicurezza, NIS2 |
| AI Champion | DA DEFINIRE (uno per team) | Primo supporto ai colleghi, raccolta feedback |
| Rete di supporto | Partecipanti gilda AI | Secondo livello di supporto, materiali |

## 8. Riepilogo dei punti aperti

> Questa sezione è un riepilogo sintetico dei punti marcati nel documento (da decidere, da verificare, da esplorare, da approfondire, da produrre). Per il dettaglio fanno fede i capitoli richiamati.

- **Budget (§2.5, §2.6)**: conferma della ricarica con Diego Moretti; fatturazione (modalità, valuta); popolazione target; mantenimento di Copilot fino a fine anno.
- **Workspaces (§3.1)**: mappa e naming, chi amministra (superadmin).
- **Guardrails (§3.2)**: politica per persona/team/mix e relativi valori.
- **Modelli EU e routing (§3.3, §6)**: conferma EU-only e ZDR con Pasquale; mappa dei modelli per caso d'uso; white-list e regole sull'auto-router.
- **Classifier (§3.4)**: nuovi classificatori, dashboard e reportistica (all'attenzione di Francesco Trucchia, CTO).
- **Chiavi API (§3.5)**: ciclo di vita e rotazione; disabilitare BYOK; logging e tracciabilità NIS2.
- **Roll out (§4.1)**: ordine di onboarding, dipendenze e criteri di ingresso; sottoscrizione del piano e del budget con Diego Moretti.
- **Percorsi di integrazione (§4.2)**: ricerca e guide how-to per A/B/C/D.
- **Formazione (§4.3)**: contenuti, durata, formato.
- **AI Champion (§4.4)**: selezione, riconoscimento, carico, canale.
- **Misurazione dell'impatto (§5.2, §5.4)**: indicatori, cadenza, soglie (all'attenzione di Francesco Trucchia, CTO).
- **Comunicazione (§4.5)**: piano e gestione del cambiamento.

## 9. Riferimenti

- [SSR - OpenRouter](ssr-adozione-openrouter.md)
- [Report finale: sperimentazione OpenRouter](report-finale-openrouter.md)
- [Pitch: adozione OpenRouter](pitch-adozione-openrouter.md)
- [Qualifica Fornitore e DPIA - OpenRouter Enterprise](https://madisoft.atlassian.net/wiki/spaces/TIS/pages/528023559) (PG-PUR-01/OR-2026)
- [Modelli disponibili in regione EU](https://openrouter.ai/models?region=eu)
- [OpenRouter Documentation Portal](https://openrouter.ai/docs/)
- [Offerta OpenRouter per Madisoft](https://docs.google.com/document/d/1UBShAQGmeq83RXyu8H53sxSQqabjQFiO)
