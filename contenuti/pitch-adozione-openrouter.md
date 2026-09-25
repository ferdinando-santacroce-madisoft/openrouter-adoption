# Pitch: adozione OpenRouter

**Adozione di OpenRouter come AI Gateway aziendale**

**Data:** 02/07/2026
**Autore / Owner:** Ferdinando Santacroce
**Responsabile Iniziativa (PM/EM):** Ferdinando Santacroce

## Problema / Opportunità

- **Qual è il problema da risolvere?** GitHub Copilot vincola i nostri team a un ecosistema rigido e a modelli predefiniti. Questa scelta ci nega l'accesso ai migliori LLM "Open Weights" di frontiera (come DeepSeek o GLM). Inoltre, non abbiamo visibilità sui consumi né controllo sulle spese: l'allocazione delle risorse AI è inefficiente.
- **Qual è l'opportunità che vogliamo cogliere?** Aumentare qualità e quantità di sviluppo supportato dall'AI. Introdurre un gateway AI unificato (OpenRouter) sblocca l'accesso a oltre 400 modelli. Con un incremento dei token disponibili e la condivisione di approcci tra dev (grazie anche alle gilde in corso), si prevede un impatto positivo sull'output dei team. Questa flessibilità permette di accelerare i task più complessi e time-consuming, come analisi per il disaccoppiamento di moduli e componenti, la ristrutturazione della suite di test del monolite "Nuvola" e la transizione verso "Nuvola 3.0".
- **Fattibilità:** una valutazione preliminare interna condotta con il Team CyberSecurity (nella persona di Pasquale Siciliano) non ha evidenziato alcun blocker tecnico o di sicurezza nell'architettura di OpenRouter.

## Perché farlo ora

- **Urgenza:** siamo nel pieno della roadmap "Verso Nuvola 3.0", con la necessità stringente di individuare azioni per rendere i team indipendenti. Più aspettiamo a sbloccare modelli specializzati nel coding, più tempo spenderemo in attività manuali ripetitive e a basso valore.
- **Cosa succede se non lo facciamo adesso?** Rimarremo legati al vendor lock-in tecnologico ed economico dei provider attuali. Mancheremo l'efficienza sui flussi operativi complessi e subiremo un rallentamento nel refactoring architetturale del monolite.
- **Collegamento con obiettivi strategici / OKR aziendali:**
  - **Objective:** ammodernamento Architetturale e Qualità del Software (Engineering Tech Strategy 2026-2028).
  - **Investment Category (Balance Framework):** Strategic. Si configura come un'attività di Enabling & Capability Building e Debt Management (refactoring verso bounded context separati, automazioni interne, miglioramento della Developer Experience).

## Soluzione proposta

- **Descrizione della soluzione ad alto livello:** avviare una fase di sperimentazione estesa a 5 sviluppatori per 1-2 mesi, utilizzando un budget iniziale pre-caricato per testare OpenRouter all'interno dei flussi reali di sviluppo (IDE, estensioni, script CLI). Al termine della prova, se i dati e le impressioni sul campo confermeranno l'efficacia, l'azienda sposterà progressivamente il budget ricorrente di 20$/mese attualmente allocato su Copilot direttamente verso il panel OpenRouter del team.
- **Alternative considerate e scartate:**
  - Mantenimento di GitHub Copilot: scartato perché troppo rigido; non permette di cambiare istantaneamente il modello sottostante e manca di un back-office avanzato per la segregazione chirurgica degli ambienti di dev/test.
  - Integrazione con OpenCode: provider dalle caratteristiche simili a OpenRouter; il back-office è meno maturo, non ha modelli con EU Residency.
  - Integrazione diretta con le API dei singoli vendor (OpenAI, Anthropic): scartata perché comporterebbe un effort di manutenzione elevato delle chiavi e del codice di integrazione, oltre al rischio di frammentazione del fatturato.
- **Deliverable principali attesi:**
  - Setup dell'organizzazione OpenRouter aziendale.
  - Configurazione del primo Workspace con tracciamento analitico indipendente.
  - Report finale post-sperimentazione con metriche di ROI e confronto qualitativo rispetto a Copilot.

## Stakeholder coinvolti

- **Interni:**
  - **Team di Sviluppo:** utilizzatori diretti e valutatori della qualità dei modelli.
  - **Ferdinando Santacroce:** project Owner e responsabile dell'iniziativa.
  - **Francesco Trucchia (CTO):** approvatore del budget aziendale e garante della coerenza con la Tech Strategy.
  - **Team IT & Security:** consultato per gli aspetti di data residency e privacy (modelli in EU e policy Zero Data Retention).
- **Esterni:** nessuno.

## Impatto atteso

- **KPI / metriche che vogliamo muovere:**
  - Incremento della velocità di rilascio sui task di refactoring (riduzione dei tempi del 20%).
  - Zero incrementi di costo: mantenimento del tetto massimo di spesa di 20$/mese per dev in caso di rollout completo.
  - 100% di conformità alla privacy impostando filtri di routing nativi EU e Zero Data Retention.
- **Benefici:**
  - **Tecnologia:** flessibilità assoluta basata su un singolo endpoint standardizzato compatibile con OpenAI SDK.
  - **Business:** ottimizzazione finanziaria e azzeramento del Vendor Lock-in; gestione elastica del budget a disposizione, che può aumentare o diminuire a piacere.
  - **Developer Experience:** interfaccia di amministrazione completa con gestione capillare di seats, cap finanziari e guardrail operativi.
- **Rischi o trade-off da considerare:**
  - Back-office: curva di apprendimento iniziale per configurare workspace (bassa).
  - Dev: configurazione dei tool di sviluppo tramite chiavi API dedicate (sforzo minimo).

## Piano iniziale

- **Timeline stimata (alto livello):**
  - **Luglio 2026:** approvazione del pitch, attivazione account dell'organizzazione e avvio della sperimentazione.
  - **Agosto 2026:** raccolta dati, retrospettiva e decisione sul rollout a tutta ingegneria.
- **Data di commitment:** 15/07/2026 (completamento setup tecnico e avvio dei test su 5 posizioni). **Livello di confidence:** Alta (90%).
- **Prossimi passi immediati:**
  1. Richiesta formale e approvazione dei 200$ di budget per i primi due mesi di trial.
  2. Creazione del Workspace "Dev" su OpenRouter e generazione delle chiavi API separate per i membri del team pilota.
- **Checkpoint:** retrospettiva tecnica e finanziaria a 30 giorni dall'inizio dei test per valutare i consumi medi reali e l'efficacia dei modelli di coding abilitati.

## Riferimenti

- [Software Selection Record (SSR) - OpenRouter](ssr-adozione-openrouter.md)
- [Report finale: sperimentazione OpenRouter](report-finale-openrouter.md)
- [Offerta OpenRouter per Madisoft](https://docs.google.com/document/d/1UBShAQGmeq83RXyu8H53sxSQqabjQFiO)
- [OpenRouter Documentation Portal](https://openrouter.ai/docs/)
- [DPA OpenRouter](https://docs.google.com/document/d/1_mKzFKAQ0Ta5tnMwM0VXzGwGpe8BhbFD/edit) (EU Processing Commitments): vedi clausole su Zero Data Retention e Infrastruttura EU/EEA.
- [Qualifica Fornitore e DPIA - OpenRouter Enterprise](https://madisoft.atlassian.net/wiki/spaces/TIS/pages/528023559) (codice PG-PUR-01/OR-2026).

### Nota di Compliance Aziendale (Policy Tracking Iniziative)

> 1. Una volta approvato il presente Pitch, creare l'**Epica su Jira** inserendo nel campo Investment Category il valore **"Strategic"**.
> 2. L'epica Jira deve obbligatoriamente contenere i link a questo documento e all'iniziativa su Swarmia.
> 3. Trattandosi di un'iniziativa con data di commitment e livello di confidence esplicitati, lo stato iniziale nella Obeya Room sarà impostato su **Iniziativa Puntuale (Verde)**. Gli aggiornamenti di stato andranno pubblicati ogni martedì durante il rituale del Planning Review.

<!-- CONFLUENCE-LOCAL-ONLY -->
### Da definire (nota interna, non pubblicata)

Per finalizzare la documentazione ed eventualmente preparare il Software Selection Record (SSR) formale da sottoporre al Board:

> 1. Chi sono esattamente gli altri 3-4 sviluppatori che prenderanno parte alla sperimentazione di 1-2 mesi? Possiamo già indicare i loro team di appartenenza (es. Atena, Platform)?
> 2. Quali saranno gli strumenti o IDE specifici attualmente in uso (es. VS Code, Cursor, IntelliJ) su cui integreremo l'API di OpenRouter durante i test?
> 3. Vuoi che generi direttamente anche la bozza del Software Selection Record (SSR) compilando la matrice comparativa dei requisiti (Must-Have/Nice-to-Have) basandoci sulla Software Selection Policy aziendale?
<!-- /CONFLUENCE-LOCAL-ONLY -->
