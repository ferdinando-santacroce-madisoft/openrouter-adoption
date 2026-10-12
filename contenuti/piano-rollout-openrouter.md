# Piano di rollout: adozione OpenRouter

## Scheda documento

| Campo | Valore |
| :---- | :---- |
| Titolo | Piano di rollout: adozione OpenRouter |
| Versione | 0.5 |
| Data | 12/10/2026 |
| Autore / Owner | Ferdinando Santacroce |
| Destinatari | Diego Moretti (CEO), Francesco Trucchia (CTO), Pasquale Siciliano (IT & Security), team di sviluppo |
| Stato | APPROVATO: avvio operativo dal 13/10/2026 |
| Classificazione | Riservato: uso interno |
| Documenti correlati | [SSR - OpenRouter](ssr-adozione-openrouter.md), [Report finale: sperimentazione OpenRouter](report-finale-openrouter.md), [Pitch: adozione OpenRouter](pitch-adozione-openrouter.md) |

## Cronologia revisioni

| Versione | Data | Autore | Descrizione |
| :---- | :---- | :---- | :---- |
| 0.1 | 25/09/2026 | Ferdinando Santacroce | Prima ossatura del piano: capitoli, stima di budget e marcatori sui punti da esplorare. |
| 0.2 | 01/10/2026 | Ferdinando Santacroce | Aggiunta l'attività di studio e analisi per l'integrazione OpenRouter - Swarmia (§4.1, §5.5), il principio guida in §5 (Swarmia come unico cruscotto) e il relativo punto aperto. |
| 0.3 | 07/10/2026 | Ferdinando Santacroce | Adeguata la fee di ricarica all'8% (piano Business, routing EU-only e ZDR): aggiornati fabbisogno 2026 e stima 2027 (§2.2, §2.3, §2.4, §2.5). |
| 0.4 | 08/10/2026 | Ferdinando Santacroce | Aggiunto il tema della review automatica delle PR come funzionalità Copilot da rimpiazzare (§2.1, §4.6, §6, §8). |
| 0.5 | 12/10/2026 | Ferdinando Santacroce | Approvazione del piano in riunione. Confermate le 25 persone come popolazione target (in valutazione l'estensione a product manager, con eventuale integrazione di budget); Copilot mantenuto in parallelo fino a fine anno con checkpoint a fine novembre; confermate data residency EU e ZDR (§3.3); kickoff di rollout fissato al 13/10 con gli sperimentatori e gli AI Champion; confermato lo studio per il rimpiazzo della review automatica delle PR (§4.6). |

## 1. Scopo del documento

Dopo la sperimentazione e la decisione di proseguire, questo documento definisce il piano operativo per introdurre OpenRouter in azienda. Non ripete la valutazione tecnica e di sicurezza, già coperta da SSR e Report finale, ma ne traduce le conclusioni in azioni: budget, configurazione della piattaforma, roll out e formazione, misurazione dell'impatto.

Il piano copre sia la parte economica e di indirizzo sia la parte esecutiva. Dove serve una conferma esplicita, il punto è marcato con un richiamo all'attenzione del soggetto competente.

Il piano è stato **approvato in riunione il 12/10/2026**. L'avvio operativo inizia con il kickoff del 13/10/2026, con i partecipanti alla sperimentazione e gli AI Champion.

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
- Popolazione assunta: **25 persone** (popolazione target confermata; in valutazione l'estensione a product manager, con eventuale integrazione di budget).
- Costo ricorrente: 25 x 20 $ = **500 $/mese**, pari a **6.000 $/anno**.
- L'abbonamento non copre solo l'IDE: include anche funzioni lato GitHub (review automatica e su richiesta delle PR, Copilot Chat, coding agent). Dismettendo Copilot si spengono tutte insieme; vanno censite e rimpiazzate (vedi §4.6).

### 2.2 Come funziona il costo di OpenRouter

OpenRouter non ha un abbonamento per persona. Il modello è diverso da Copilot:

- Si **caricano crediti** una volta (pagamento anticipato) e i crediti vengono consumati in base all'uso reale (pay-as-you-go).
- La stessa ricarica può essere **ripartita a piacere** tra gli utilizzatori, tramite workspace e chiavi API dedicate.
- È prevista una **fee di piattaforma dell'8%** sul momento della ricarica dei crediti. La fee sale dal 5,5% all'8% con il passaggio al piano Business, lo stesso che abilita il routing EU-only e la Zero Data Retention.
- Il costo dipende dal modello scelto e dal routing (con l'istruzione `:floor` si può puntare al fornitore momentaneamente più economico).

Conseguenza pratica: la richiesta non è una licenza a testa, ma una **ricarica di credito** con cui coprire l'equivalente del budget attuale.

### 2.3 Fabbisogno per il 2026 (ottobre-dicembre)

Per semplicità si considerano i tre mesi che restano da qui a fine 2026: ottobre, novembre e dicembre.

| Voce | Calcolo | Valore |
| :---- | :---- | :---- |
| Inferenza equivalente | 25 dev x 20 $ x 3 mesi | 1.500 $ |
| Fee di ricarica 8% | 1.500 $ x 8% | 120 $ |
| **Ricarica consigliata 2026** | arrotondamento al successivo multiplo di 50 | **~1.650 $** |

### 2.4 Stima per il 2027

| Voce | Calcolo | Valore |
| :---- | :---- | :---- |
| Inferenza equivalente | 25 dev x 20 $ x 12 mesi | 6.000 $ |
| Fee di ricarica 8% | 6.000 $ x 8% | 480 $ |
| **Ricarica consigliata 2027** | arrotondamento al successivo multiplo di 50 | **~6.500 $** |

### 2.5 Sintesi della richiesta

| Periodo | Copilot (status quo) | OpenRouter (equivalente + fee) |
| :---- | :---- | :---- |
| Ottobre-dicembre 2026 | 1.500 $ | ~1.650 $ |
| Anno 2027 | 6.000 $ | ~6.500 $ |

L'iniziativa è **sostanzialmente neutra**: non aggiunge un costo nuovo, ma **sposta** il budget ricorrente oggi allocato su Copilot verso OpenRouter. L'unica differenza, con il piano Business, è la fee di ricarica dell'8% (120 $ per il trimestre 2026, 480 $ su base annua) e il periodo di sovrapposizione dei due strumenti, previsto fino a fine anno (§2.6).

### 2.6 Ipotesi, decisioni e variabili da verificare

> **RISOLTO**: le 25 persone sono la **popolazione target** del rollout. È in valutazione l'estensione ai product manager. Vista la natura del servizio, possiamo aggiungere e togliere persone quando vogliamo, ricalibrando il budget.
> **RISOLTO**: Copilot resta in parallelo **fino a fine anno**. A novembre 2026 un punto della situazione per decidere se dismetterlo definitivamente o mantenerlo.
> **DA VERIFICARE**: fatturazione (modalità, valuta, etc.).

## 3. Piano di configurazione di OpenRouter

### 3.1 Organizzazione e Workspaces

Ipotesi di partenza: un **workspace per team** (prodotto, platform, IT&Security, Staff+).

> **DA DEFINIRE**: numero e mappa dei workspace; naming convention; chi amministra i workspace (il "superadmin" di turno); come gestire account di persone che non fanno parte di un team (ad es. account di Francesco T. e Diego, eventuali account per designer, etc.). Questi punti si definiscono nella riunione di kickoff del 13/10/2026, con i partecipanti alla sperimentazione e gli AI Champion.

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

> **CONFERMATO**: data residency in Europa e Zero Data Retention confermate (riunione del 12/10/2026). Il piano Business si sottoscrive con routing EU-only e ZDR contrattuale; responsabile Pasquale Siciliano.

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
| 2 | Kickoff (13/10), comunicazione e configurazione guardrails e workspace | Ottobre 2026 | F. Santacroce |
| 3 | Onboarding dei team e distribuzione chiavi | Ottobre 2026 | F. Santacroce + AI Champion |
| 4 | Formazione iniziale e materiali how-to | Ottobre 2026 | F. Santacroce + AI Champion |
| 5 | Spostamento del budget ricorrente da Copilot a OpenRouter | Al rollout | F. Santacroce + Diego Moretti |
| 6 | Monitoraggio consumi e checkpoint periodici | Continuo | F. Santacroce + Francesco Trucchia |
| 7 | Studio e analisi di fattibilità per l'integrazione OpenRouter - Swarmia (raccolta dei dati d'uso per le metriche AI) | Novembre 2026 | F. Santacroce + Francesco Trucchia |

> **RISOLTO**: il kickoff del rollout si tiene il **13/10/2026** con i partecipanti alla sperimentazione e gli AI Champion; in quell'occasione si definiscono workspace, naming convention e organizzazione (§3.1, §4.4). Resta da approfondire l'ordine di onboarding dei team, le dipendenze e i criteri di ingresso per ciascuna fase (i criteri di uscita del rollout sono in 1.2).
> **Con Diego**: sottoscrizione del piano Business (routing EU-only e ZDR). Budget approvato in riunione, con eventuale integrazione in caso di estensione della popolazione.

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

> **IN DEFINIZIONE**: la lista degli AI Champion per team sarà stabilita nella riunione del 13/10/2026; alcune persone si sono già offerte volontarie, altre vanno sollecitate a proporsi.
> **DA DECIDERE**: criteri di selezione dell'AI Champion; come si riconosce il ruolo; carico atteso; canale di comunicazione (es. canale Slack dedicato); come si raccolgono i problemi ricorrenti per trasformarli in FAQ e guide.

### 4.5 Comunicazione e gestione del cambiamento

> **DA APPROFONDIRE**: piano di comunicazione (perché cambiamo, cosa cambia per i dev, cosa resta), gestione delle aspettative e dei casi d'uso, gestione del doppio strumento durante la transizione.

### 4.6 Funzionalità Copilot da rimpiazzare: review automatica delle PR

La dismissione di GitHub Copilot non spegne solo il completamento in IDE. L'abbonamento include funzioni usate in modo trasversale, prima fra tutte la **review automatica delle PR** direttamente su GitHub. Diversi sviluppatori la usano come primo filtro sulle pull request (ne è testimonianza la nota di Lorenzo Piersante riportata nel Report finale). Poiché Copilot resta attivo fino a fine anno (§2.6), la review continua a funzionare: il tempo a disposizione serve a decidere se replicare la funzionalità o abbandonarla.

**Verifiche da fare:**

- censire quali funzioni Copilot oltre all'IDE sono in uso (review automatica e su richiesta sulle PR, Copilot Chat su GitHub, coding agent sulle issue) e da chi;
- stabilire cosa si perde esattamente alla disattivazione dell'abbonamento e con quale impatto sui flussi di review.

**Alternative da valutare:**

- **tooling esterno** di code review (ad es. CodeRabbit, Greptile, Qodo Merge / PR-Agent): da confrontare su costo, residenza dei dati (EU/ZDR), integrazione con GitHub e qualità delle review;
- **soluzione interna** in pipeline CI che chiama un modello via OpenRouter: il Report finale documenta un esperimento interno di PR review agentica via API (es. Kimi 3), con esito positivo su PR corpose. Riprende il tema già aperto nella SSR (Temi aperti dai commenti di revisione);
- **skill personali o agenti** che usano l'inferenza di OpenRouter, come alternativa leggera al tooling dedicato.

> **DA VERIFICARE**: funzioni Copilot oltre l'IDE effettivamente in uso e cosa si perde con la dismissione (review automatica delle PR in primis). Con Copilot mantenuto fino a fine anno, la verifica può procedere senza urgenza.
> **DA DECIDERE**: se replicare la review automatica delle PR (tooling esterno o pipeline interna su OpenRouter) oppure abbandonarla in favore di sistemi alternativi, ad esempio skill personali o agenti che usano l'inferenza di OpenRouter; definire il relativo owner.

## 5. Misurazione di adozione e impatto

Principio guida: vogliamo che Swarmia resti l'unico strumento su cui i team osservano la salute e le performance, e che anche le metriche d'uso degli strumenti di intelligenza artificiale entrino a far parte di quel set. L'adozione di OpenRouter non deve vivere in una dashboard separata, ma diventare una delle dimensioni che i team già guardano e monitorano abitualmente. Per questo l'integrazione descritta in §5.5 è il perno della misurazione: porta i dati d'uso di OpenRouter dentro lo stesso cruscotto con cui leggiamo delivery e produttività.

### 5.1 Metriche di adozione

- Utilizzatori attivi per team e per workspace.
- Chiavi attive e consumi per modello e per caso d'uso.
- Distribuzione dei livelli di autonomia (classifier) e dei tipi di lavoro.
- Lettura di queste metriche dentro Swarmia, accanto a quelle di delivery già monitorate dai team (vedi §5.5).

### 5.2 Metriche di impatto sulla produttività

> **DA ESPLORARE**: quali indicatori usare e con quale cadenza, per valutare se lo strumento ha un impatto positivo, neutro o negativo. Piste da valutare: lead time e throughput delle PR, tempo su refactoring e test, spesa per PR, qualità (difetti), affiancamento a pratiche di pair/mob programming. Le metriche aggregate per team sono il livello di lettura preferito.

### 5.3 Strumenti e fonti

- Dashboard OpenRouter per workspace (consumi e modelli).
- Classificatori OpenRouter (autonomia, tipo di lavoro).
- Jira e GitHub per throughput e lead time.
- Swarmia (integrazione custom, vedi §5.5).
- Survey periodica di soddisfazione.

### 5.4 Cadenza dei checkpoint

> **DA DECIDERE**: frequenza dei checkpoint (mensile magari all'inizio, poi trimestrale), chi analizza i dati, a chi vengono riportati e quali soglie fanno scattare correzioni.

### 5.5 Integrazione con Swarmia: studio di fattibilità

Obiettivo: capire come riversare in Swarmia i dati d'uso di OpenRouter, così che adozione e impatto dell'AI si leggano nella stessa piattaforma in cui l'azienda misura già produttività e delivery. Swarmia offre due funzionalità rilevanti:

- la scheda **ROI** in *AI impact*: mette a confronto ciò che i team consegnano e i costi sostenuti (costo per storia o epica, per PR, per riga modificata), con lettura per team;
- i **custom AI tools**: permettono di aggiungere uno strumento AI non nativo in due modi: collegando l'account Git del tool (se fa commit e review con un'identità propria) oppure inviando all'API di Swarmia i dati d'uso giornalieri per utente, inclusi costo, modello e token. OpenRouter, in quanto gateway e non coding tool con identità Git propria, ricade con ogni probabilità nel secondo caso.

Attività dello studio:

- verificare quali dati d'uso espone OpenRouter per utente e per chiave (token, costo, modello, timestamp) e con quale granularità;
- definire la mappatura tra identità OpenRouter e utenti Swarmia;
- valutare se, oltre ai consumi, sia possibile ricostruire anche le metriche di contributo (commit, PR) riconducibili all'uso di OpenRouter;
- stabilire quali metriche di adozione (§5.1) e di impatto (§5.2) sono effettivamente derivabili da questa integrazione.

Output atteso: nota di fattibilità con l'architettura dell'integrazione (raccolta dati da OpenRouter verso l'API custom di Swarmia), la stima dello sforzo e l'eventuale piano di realizzazione.

> **DA ESPLORARE**: fattibilità tecnica dell'integrazione OpenRouter - Swarmia e mappatura delle identità; quali dati inviare via API custom. Riferimenti: [ROI dei tool AI](https://www.swarmia.com/changelog/2026-08-07-ai-roi/), [custom AI tools](https://www.swarmia.com/changelog/2026-08-19-custom-ai-tools/).

## 6. Rischi e mitigazioni

| Rischio | Mitigazione |
| :---- | :---- |
| Sforamenti di spesa per configurazioni errate | Default workspace a zero; verifica ereditarietà chiavi; cap per team e per persona |
| Selezione di modelli costosi via auto-router | White-list modelli e uso di `:floor` |
| Disomogeneità dei provider sullo stesso modello | Test di reattività prima dell'adozione per team |
| Logging e tracciabilità (NIS2) contro rischi di privacy | Decisione formale condivisa con Pasquale |
| Sovrapposizione Copilot e OpenRouter durante la transizione | Copilot mantenuto fino a fine anno; checkpoint a novembre 2026 per la dismissione definitiva |
| Perdita della review automatica delle PR con la dismissione di Copilot | Censimento delle funzioni in uso; alternativa con tooling esterno o pipeline interna su OpenRouter (§4.6) |
| Adozione disomogenea tra i team | AI Champion per team e guide how-to dedicate |

## 7. Ruoli e responsabilità

| Ruolo | Persona | Responsabilità |
| :---- | :---- | :---- |
| Owner dell'iniziativa | Ferdinando Santacroce | Piano, budget, configurazione, coordinamento |
| Sponsor tecnico | Francesco Trucchia (CTO) | Indirizzo, coerenza con la Tech Strategy, metriche |
| Approvatore budget | Diego Moretti (CEO) | Budget di spesa preventivata |
| IT & Security | Pasquale Siciliano | Conformità EU/ZDR, sicurezza, NIS2 |
| AI Champion | IN DEFINIZIONE: lista il 13/10/2026 (uno per team) | Primo supporto ai colleghi, raccolta feedback |
| Rete di supporto | Partecipanti gilda AI | Secondo livello di supporto, materiali |

## 8. Riepilogo dei punti aperti

> Questa sezione è un riepilogo sintetico dei punti marcati nel documento (da decidere, da verificare, da esplorare, da approfondire, da produrre, in definizione). Per il dettaglio fanno fede i capitoli richiamati.

- **Budget (§2.5, §2.6)**: fatturazione (modalità, valuta); eventuale integrazione di budget se la popolazione si estende ai project manager e ai product manager. Popolazione target (25) confermata; Copilot mantenuto fino a fine anno.
- **Workspaces (§3.1)**: mappa e naming, chi amministra (superadmin). Da definire nella riunione del 13/10/2026.
- **Guardrails (§3.2)**: politica per persona/team/mix e relativi valori.
- **Modelli EU e routing (§3.3, §6)**: mappa dei modelli per caso d'uso; white-list e regole sull'auto-router. Routing EU-only e ZDR confermati.
- **Classifier (§3.4)**: nuovi classificatori, dashboard e reportistica (all'attenzione di Francesco Trucchia, CTO).
- **Chiavi API (§3.5)**: ciclo di vita e rotazione; disabilitare BYOK; logging e tracciabilità NIS2.
- **Roll out (§4.1)**: kickoff il 13/10/2026; ordine di onboarding, dipendenze e criteri di ingresso; sottoscrizione del piano Business con Diego Moretti.
- **Percorsi di integrazione (§4.2)**: ricerca e guide how-to per A/B/C/D.
- **Funzioni Copilot oltre l'IDE (§2.1, §4.6)**: censimento delle funzioni in uso (review automatica delle PR, Copilot Chat su GitHub, coding agent) e decisione se replicare la review automatica delle PR (tooling esterno o pipeline interna su OpenRouter) oppure abbandonarla in favore di skill personali o agenti su OpenRouter.
- **Formazione (§4.3)**: contenuti, durata, formato.
- **AI Champion (§4.4)**: lista nella riunione del 13/10/2026; criteri di selezione, riconoscimento, carico, canale.
- **Misurazione dell'impatto (§5.2, §5.4)**: indicatori, cadenza, soglie (all'attenzione di Francesco Trucchia, CTO).
- **Integrazione Swarmia (§5.5)**: studio di fattibilità per riversare i dati d'uso di OpenRouter nelle metriche AI di Swarmia (attività di novembre 2026).
- **Comunicazione (§4.5)**: piano e gestione del cambiamento.

## 9. Riferimenti

- [SSR - OpenRouter](ssr-adozione-openrouter.md)
- [Report finale: sperimentazione OpenRouter](report-finale-openrouter.md)
- [Pitch: adozione OpenRouter](pitch-adozione-openrouter.md)
- [Qualifica Fornitore e DPIA - OpenRouter Enterprise](https://madisoft.atlassian.net/wiki/spaces/TIS/pages/528023559) (PG-PUR-01/OR-2026)
- [Modelli disponibili in regione EU](https://openrouter.ai/models?region=eu)
- [OpenRouter Documentation Portal](https://openrouter.ai/docs/)
- [Offerta OpenRouter per Madisoft](https://docs.google.com/document/d/1UBShAQGmeq83RXyu8H53sxSQqabjQFiO)
