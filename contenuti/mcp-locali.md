# 1. Premessa: un server MCP è una tecnologia, non un fornitore

Questo documento nasce da un fraintendimento comune: un server MCP viene talvolta trattato come un fornitore esterno a cui comunichiamo dei dati, al pari di un provider di inferenza. Sono due cose diverse e vanno tenute separate.

Un server MCP è una tecnologia: un programma che espone delle capacità a un assistente AI. Non è un soggetto terzo a cui inviamo dati, è un programma che gira sul PC in locale esattamente come Git o un qualsiasi IDE. La domanda "chi è questo fornitore e quali garanzie ci dà" non si applica a un server MCP in sé.

La distinzione che conta non è "usiamo o no un server MCP", ma dove finiscono i dati: restano sulla postazione, oppure transitano verso un servizio terzo?

# 2. Come funzionano gli MCP e il ruolo dell'harness agentica

## 2.1 Cos'è un server MCP

MCP (Model Context Protocol) è uno standard che definisce come un programma esterno può mettere a disposizione di un assistente AI delle capacità: funzioni che l'assistente può invocare (tool), dati che può leggere (risorse), istruzioni predefinite (prompt).

Un server MCP è un processo che implementa questo standard. CodeGraph e TokenSave sono server MCP: espongono funzioni come "cerca questo simbolo nel codice" o "mostra le dipendenze di questo file". Non sono modelli: non "ragionano", eseguono solo ciò che viene loro richiesto, come un qualsiasi programma tradizionale.

È quindi una tecnologia, non un fornitore: un programma al pari di Git, di un IDE o di un qualsiasi altro strumento di sviluppo.

## 2.2 Il flusso, passo per passo

- Lo sviluppatore avvia l'harness, che legge la configurazione e avvia/si connette ai server MCP dichiarati.
- Ogni server MCP dichiara all'harness quali funzioni offre e con quali parametri.
- L'harness invia al modello, insieme al messaggio dello sviluppatore, anche l'elenco di queste funzioni, come "strumenti disponibili".
- Il modello non esegue nulla direttamente: quando lo ritiene utile, restituisce una richiesta strutturata del tipo "vorrei chiamare la funzione X con questi parametri". È solo testo.
- È l'harness a intercettare questa richiesta e a inoltrarla davvero al server MCP corrispondente, che la esegue sulla macchina locale.
- Il risultato torna all'harness, che lo restituisce al modello come nuovo contesto, e il ciclo prosegue.

## 2.3 Perché il modello non parla mai direttamente con l'MCP

Un LLM riceve solo testo (le funzioni disponibili, come schema) e restituisce solo testo (la richiesta di chiamata, come dato strutturato). Non ha una connessione di rete propria né esegue codice proprio.

Chi esegue davvero la chiamata è sempre l'harness, con i privilegi che lo sviluppatore ha concesso. È un punto rilevante dal punto di vista architetturale: qualunque controllo (permessi, conferma dell'utente, criteri aziendali) va applicato a questo livello, perché il modello non ha modo di applicarlo da sé.

## 2.4 Il trasporto locale

Server MCP locali girano come processi separati sulla stessa macchina dello sviluppatore, avviati direttamente dall'harness, che comunica con loro tramite standard input/output (trasporto detto "stdio"). Significa che il server MCP eredita gli stessi privilegi dell'utente che ha avviato l'harness: stesso accesso al filesystem, alle variabili d'ambiente, alla rete.

Finché il server gira in locale e tiene i dati sulla macchina, questi non escono: resta sullo stesso piano di un sistema di versionamento del codice (Git), di un IDE (PhpStorm, Visual Studio Code) o di qualsiasi altro strumento installato sulla postazione. 

## 2.5 Chi applica i controlli

Il protocollo MCP definisce come uno strumento viene dichiarato e invocato, ma non impone come una specifica harness debba gestire permessi o conferme. Ogni harness decide autonomamente quali server MCP può avviare, quali funzioni richiedono conferma esplicita dello sviluppatore e quali vengono eseguite senza chiederla. È per questo che la stessa configurazione MCP può comportarsi in modo diverso a seconda di quale harness la esegue.

# 3. Quando un server MCP diventa un fornitore esterno

Il quadro cambia se il server MCP non lavora solo in locale, ma fa da ponte tra il modello e un servizio terzo: ad esempio un server MCP di Shopify che legge e scrive dati su Shopify. In quel caso i dati transitano verso l'esterno ed entrano in possesso di un soggetto terzo, esattamente come accadrebbe con un provider di inferenza.

È quel soggetto (Shopify nell'esempio), non il server MCP in sé, a dover essere censito come fornitore esterno, con le clausole di garanzia e contrattuali del caso. Il server MCP resta il mezzo tecnico; il fornitore è il servizio a cui i dati arrivano.

# 4. Il caso dei nostri MCP locali (CodeGraph e TokenSave)

Pasquale ci segnala: i repository GitHub di CodeGraph e TokenSave riportano vulnerabilità aperte, non ancora corrette. Le perplessità sull'uso di questi due server MCP nascono da lì.

Il punto da chiarire è che, una volta stabilito che un server MCP locale è uno strumento di sviluppo al pari di un IDE o di un client Git, le vulnerabilità sono da trattare al pari di tutti i software installati sulla postazione dello sviluppatore. Tutti gli strumenti di sviluppo hanno bug e vulnerabilità: PhpStorm ne ha, Visual Studio Code ne ha, e ne ha perfino il sistema operativo, Linux e Ubuntu compresi. Applicare ai server MCP un criterio che non applichiamo agli altri strumenti che usiamo ogni giorno significherebbe riservare loro un trattamento speciale: serve una ragione.

La differenza rilevante l'abbiamo già messa a fuoco: un server MCP locale non ha per scopo quello di mandare dati all'esterno. I suoi eventuali problemi restano confinati alla postazione, come quelli di qualsiasi altro programma installato. Per questo crediamo che le sue vulnerabilità siano accettabili nella stessa misura in cui consideriamo accettabili quelle di un IDE, di un client Git o del sistema operativo.

Quello che ci serve sapere quali sono le policy di utilizzo del software locale.

## 4.1 Postilla: la policy di installazione dei software locali

Che tipo di policy abbiamo sull'installazione di software locale?

Sulle postazioni è attivo l'XDR di Trend Micro, che però oggi non censisce i programmi: li monitora. Non esiste, ad oggi, una whitelist di programmi ammessi né una blacklist di programmi vietati; l'XDR osserva tutti i programmi in esecuzione.

La domanda da dipanare con Pasquale riguarda quindi il comportamento, non il censimento. Se domani uno sviluppatore installa un server MCP locale come TokenSave e quel server, per qualche motivo, viene corrotto, "impazzisce" o comincia a fare cose strane, quel comportamento anomalo o malevolo verrebbe intercettato dall'XDR? In altri termini, possiamo contare sulla stessa protezione che ci aspettiamo per qualsiasi altro software che usiamo: tutti i programmi, a pagamento o meno, possono essere corrotti, infettati da una backdoor o compromessi allo stesso modo.

Per quanto ne sappiamo oggi l'installazione di strumenti di sviluppo locali è piuttosto libera: gli sviluppatori possono installare i tool di cui hanno bisogno senza particolari problemi. I tool devono avere licenza aziendale se a pagamento; per quelli open source, a oggi, non risultano regole o linee guida specifiche. Se resta così, ogni sviluppatore è libero di installarsi piccoli strumenti di sviluppo in locale senza chiedere permesso a nessuno, e la questione è risolta.

# 5. Esito della riunione del 1 ottobre 2026

La proposta di cui sopra è stata discussa nella riunione del 1 ottobre 2026 con Pasquale Siciliano e Davide Fossacecchi. La riunione ha confermato l'impostazione: un server MCP non è un fornitore esterno e si può usare, purché i dati non escano dal perimetro che già governiamo. Di seguito la decisione presa e il modo di utilizzare gli MCP da qui in avanti.

## 5.1 La regola da comunicare a tutti

Alla luce di quanto sopra, la regola è una sola: sono vietati i server MCP che inviano dati aziendali verso servizi terzi non censiti tra i fornitori approvati da Madisoft. Un server MCP locale, che tiene i dati sulla postazione, resta uno strumento di sviluppo ordinario e non rientra in questo divieto.

## 5.2 La decisione

L'uso dei server MCP è consentito quando soddisfa una di queste due condizioni:

- il server opera interamente in locale, senza contattare servizi esterni (ad es. CodeGraph e TokenSave)
- il server dialoga con un servizio terzo per cui Madisoft ha già un contratto o una licenza in essere (ad es. Jira, GitHub).

Fuori da questi due casi, l'uso è vietato.

## 5.3 Come si legge il criterio

Il criterio si applica in tre situazioni:

- **Dati locali.** Un server MCP che legge dati sulla postazione e li tiene lì, senza contattare servizi esterni, è uno strumento di sviluppo ordinario. È il caso di CodeGraph e TokenSave, che leggono la codebase di Nuvola e la indicizzano localmente.
- **Servizio remoto già coperto da contratto o licenza.** Un server MCP che dialoga con un servizio con cui abbiamo già un rapporto contrattuale o una licenza è ammesso. È il caso di Jira, dove leggiamo e scriviamo dati perché abbiamo contratto e licenze in essere, e di GitHub, con cui abbiamo parimenti un contratto e una licenza.
- **Servizio remoto senza contratto né licenza.** Un server MCP che manda dati a un servizio con cui non abbiamo alcun rapporto contrattuale è vietato. È il caso di Shopify o YouTube: non abbiamo un contratto né una licenza, e quei dati potenzialmente sensibili non devono uscire.

Il discrimine non è la tecnologia MCP in sé, ma dove finiscono i dati: se restano dentro il perimetro che già conosciamo e governiamo, oppure se escono verso un soggetto terzo senza copertura contrattuale.

## 5.4 La richiesta a Francesco Trucchia

Resta un punto operativo da sbloccare. GitHub applica una restrizione, a livello di organization, che impedisce di abilitare i server MCP nella configurazione gestita dall'organizzazione stessa.

Il vincolo, però, è circoscritto: riguarda solo l'abilitazione o la disabilitazione della configurazione dei server MCP così come appare nell'interfaccia gestita. Non può impedire a uno sviluppatore di avviare in locale un server MCP sul proprio computer con una configurazione scritta a mano nel file JSON. Detto altrimenti, il blocco agisce sull'interruttore della configurazione, non su ciò che gira sulla macchina: è un vincolo di facciata, che non incide sulla sostanza della sicurezza.

Chiediamo quindi a Francesco Trucchia, CTO, di sbloccare l'attivazione dei server MCP su GitHub per il periodo di transizione, in attesa del passaggio a OpenRouter. La richiesta nasce da un'esigenza concreta: senza lo sblocco, i flussi di lavoro che si appoggiano a GitHub restano vincolati da una restrizione che non cambia la sostanza, perché l'uso locale degli MCP è comunque possibile e legittimo.
