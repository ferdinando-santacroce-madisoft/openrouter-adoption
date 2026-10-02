# Parte prima: lo strumento e il suo funzionamento

## 1. Un server MCP è una tecnologia, non un fornitore

Questo documento nasce per chiarire un fraintendimento comune: un server MCP viene spesso inteso come un servizio esterno a cui comunichiamo dei dati, al pari di un provider di inferenza. Sono due cose diverse e vanno tenute separate.

Un server MCP è un programma che espone delle capacità a un assistente AI. Non è un server a cui inviamo dati, è uno strumento di sviluppo che gira localmente, come Git o un IDE. La domanda "chi è questo fornitore e quali garanzie ci dà" non si applica a un server MCP in sé.

La distinzione che conta non è se usiamo un server MCP, ma dove finiscono i dati che l'MCP server gestisce: restano sulla postazione, oppure transitano verso un servizio terzo?

## 2. Come funziona

### 2.1 Il flusso

MCP (Model Context Protocol) è lo standard con cui un sistema mette a disposizione di un assistente AI delle capacità: funzioni da invocare (tool), dati da leggere (risorse), istruzioni predefinite (prompt).

Il flusso, passo per passo:

- Lo sviluppatore avvia l'harness, che legge la configurazione e si connette ai server MCP dichiarati.
- Ogni server dichiara all'harness quali funzioni offre e con quali parametri.
- L'harness passa al modello anche l'elenco di queste funzioni, come "strumenti disponibili".
- Il modello non esegue nulla: restituisce solo una richiesta strutturata del tipo "vorrei chiamare la funzione X con questi parametri".
- L'harness intercetta la richiesta e la inoltra al server MCP, che la esegue sulla macchina locale.
- Il risultato torna al modello come nuovo contesto, e il ciclo prosegue.

### 2.2 Chi esegue, chi controlla

Un LLM riceve e produce solo testo. Non ha una connessione di rete propria né esegue codice: chi esegue davvero è sempre l'harness, con i privilegi che lo sviluppatore gli ha concesso. Il protocollo non impone come l'harness gestisca permessi e conferme; ogni harness decide quali server avviare e quali funzioni richiedere conferma. Per questo la stessa configurazione può comportarsi diversamente da un harness all'altro.

### 2.3 Il trasporto locale

Un server MCP locale gira come processo separato sulla macchina dello sviluppatore, avviato dall'harness e collegato via standard input/output ("stdio"). Eredita gli stessi privilegi dell'utente: accesso al filesystem, alle variabili d'ambiente, alla rete. Finché tiene i dati sulla macchina, questi non escono.

## 3. Quando un server MCP diventa un fornitore esterno

Il quadro cambia se il server MCP fa da ponte tra il modello e un servizio terzo: un server MCP di Shopify, per esempio, legge e scrive dati su Shopify. I dati escono e finiscono in mano a un soggetto terzo, come accadrebbe con un provider di inferenza.

È quel soggetto (Shopify), non il server MCP, a dover essere censito come fornitore esterno, con le clausole di garanzia del caso. Il server MCP resta il mezzo; il fornitore è il servizio a cui i dati arrivano.

# Parte seconda: la cronologia e le decisioni

## 4. Come siamo arrivati qui

La vicenda, in breve:

- **Rilievo.** Pasquale Siciliano, IT manager e Cyber Security, ci segnala che i repository GitHub di CodeGraph e TokenSave riportano vulnerabilità aperte, non ancora corrette.
- **Documento.** Ferdinando Santacroce e Davide Fossacecchi preparano questo documento per chiarire la questione.
- **Confronto.** Il 1 ottobre 2026 ci confrontiamo e raggiungiamo conclusioni condivise, che fissiamo qui sotto.
- **Pubblicazione.** Il 2 ottobre 2026 pubblichiamo il documento per tutta l'azienda, per chiarire l'oggetto del contendere e avviare il confronto con Francesco Trucchia sull'abilitazione dei server MCP su GitHub.

Sul rilievo di Pasquale la posizione è chiara: le vulnerabilità non sono un argomento ostativo. Tutti gli strumenti di sviluppo hanno bug: PhpStorm, Visual Studio Code, perfino il sistema operativo. Applicare ai server MCP un criterio che non applichiamo agli altri strumenti che usiamo ogni giorno significherebbe riservare loro un trattamento speciale, senza una buona ragione.

La differenza che conta è dove finiscono i dati: un server MCP locale non manda nulla all'esterno, quindi i suoi problemi restano confinati alla postazione, come quelli di qualsiasi altro programma installato. Le sue vulnerabilità sono accettabili nella stessa misura in cui lo sono quelle di un IDE o di un client Git.

### 4.1 Postilla: la policy sul software locale

Che tipo di policy abbiamo sull'installazione di software locale?

Sulle postazioni è attivo l'XDR di Trend Micro, che però oggi non censisce i programmi: li monitora. Non esiste una whitelist di programmi ammessi né una blacklist di vietati; l'XDR osserva tutti i programmi in esecuzione.

La domanda riguarda il comportamento, non il censimento: se un server MCP locale come TokenSave viene corrotto e comincia a fare cose strane, l'XDR lo intercetta? In altri termini, possiamo contare sulla stessa protezione che ci aspettiamo per qualsiasi altro software che usiamo?

Oggi l'installazione di strumenti di sviluppo locali è libera: gli sviluppatori installano i tool di cui hanno bisogno (con buon senso, evitando software di dubbia natura e provenienza). I tool a pagamento devono avere licenza aziendale; per quelli open source non risultano regole specifiche. Se resta così, ogni sviluppatore può installarsi piccoli strumenti in locale (compresi server MCP locali) senza chiedere permesso, e la questione è risolta.

## 5. La decisione

L'uso dei server MCP è consentito in due casi: il server opera interamente in locale, oppure dialoga con un servizio terzo per cui Madisoft ha già un contratto o una licenza in essere. Fuori da questi due casi, l'uso è vietato.

### 5.1 Come si legge il criterio

- **Dati locali.** Il server legge dati sulla postazione e li tiene lì, senza contattare servizi esterni. È il caso di CodeGraph e TokenSave, che leggono la codebase di Nuvola e la indicizzano localmente.
- **Servizio terzo già coperto da contratto o licenza.** Il server dialoga con un servizio con cui abbiamo già un rapporto contrattuale o una licenza. È il caso di Jira, dove leggiamo e scriviamo dati, e di GitHub.
- **Servizio terzo senza contratto né licenza.** Il server manda dati a un servizio con cui non abbiamo alcun contratto. È il caso di Shopify o YouTube: quei dati potenzialmente sensibili non devono uscire.

Il discrimine non è la tecnologia MCP, ma dove finiscono i dati: dentro il perimetro che già governiamo, oppure fuori senza copertura contrattuale.

## 6. La richiesta a Francesco Trucchia

Resta un punto da sbloccare. GitHub applica una restrizione a livello di organization che impedisce di abilitare i server MCP nella configurazione gestita.

Il vincolo è però circoscritto: riguarda solo l'interruttore della configurazione, non ciò che gira sulla macchina. Non impedisce a uno sviluppatore di avviare in locale un server MCP con una configurazione scritta a mano nel file JSON. È un vincolo di facciata, che non incide sulla sostanza della sicurezza.

Chiediamo quindi a Francesco Trucchia, CTO, di sbloccare l'attivazione dei server MCP su GitHub per il periodo di transizione, in attesa del passaggio a OpenRouter. Senza lo sblocco, i flussi di lavoro che si appoggiano a GitHub restano vincolati da una restrizione che non cambia la sostanza, perché l'uso locale degli MCP è comunque possibile e legittimo.
