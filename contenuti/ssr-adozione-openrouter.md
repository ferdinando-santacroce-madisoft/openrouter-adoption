# SSR - OpenRouter

## Scheda documento

| Campo | Valore |
| :---- | :---- |
| Codice documento | MAD.TIS.SSR.03 |
| Titolo | SSR - OpenRouter |
| Versione | 1.3 |
| Data emissione | 10/07/2026 |
| Ultimo aggiornamento | 12/10/2026 |
| Autore / Proposer | Ferdinando Santacroce |
| Revisore IT & Security | Pasquale Siciliano |
| Stato | APPROVATO |
| Classificazione | Riservato - uso interno |
| Prossima revisione | 25/09/2027, oppure prima in caso di cambio major version, licenza, vendor, modalità di esecuzione, telemetria, connettori o provider LLM. |

## Riferimenti normativi, policy e documenti correlati

- GDPR e Clausole Contrattuali Standard (SCC), Modulo 2 Controller-to-Processor, foro di Dublino (Irlanda).
- Software Selection Policy aziendale.
- [Pitch: adozione OpenRouter](pitch-adozione-openrouter.md)
- [Report finale: sperimentazione OpenRouter](report-finale-openrouter.md)
- [Qualifica Fornitore e DPIA - OpenRouter Enterprise](https://madisoft.atlassian.net/wiki/spaces/TIS/pages/528023559) (codice PG-PUR-01/OR-2026, rev. 1.0, 05/08/2026).
- IS-313: valutazione di sicurezza OpenRouter Enterprise, esito Done (Pasquale Siciliano).

## Cronologia revisioni

| Versione | Data | Autore | Descrizione |
| :---- | :---- | :---- | :---- |
| 1.0 | 10/07/2026 | Ferdinando Santacroce | Prima emissione dell'SSR. |
| 1.1 | 25/09/2026 | Ferdinando Santacroce | Aggiornamento post-sperimentazione: dati raccolti, esito security e piano di adozione. |
| 1.2 | 25/09/2026 | Ferdinando Santacroce | Recepiti i commenti di revisione del CTO sul documento originale: aggiunto il requisito di osservabilità dell'utilizzo; aperto il tema della review automatica delle PR di GitHub Copilot. |
| 1.3 | 12/10/2026 | Ferdinando Santacroce | Approvazione della soluzione in riunione (CTO e CEO): aggiornato lo stato a "APPROVATO" e la sezione Decisione finale; confermati routing EU-only e ZDR. |

## Informazioni di base

- **Titolo selezione:** Adozione OpenRouter Enterprise come gateway unificato LLM per l'ingegneria del software.
- **Proposer:** Ferdinando Santacroce.
- **Data:** 10/07/2026.
- **Business need:** centralizzare l'accesso ai modelli di Intelligenza Artificiale per i team di sviluppo, garantendo l'intercambiabilità dei modelli (evitando il vendor lock-in), il controllo granulare delle spese per ambiente e il rispetto delle normative europee sul trattamento dei dati (GDPR).

## Requisiti

| Tipo | Requisito | Priorità | Note |
| :---- | :---- | :---- | :---- |
| FR | API Endpoint standardizzato e compatibile con OpenAI SDK. | M | Essenziale per un innesto agile nei tool di sviluppo. |
| FR | Console di back-office con Workspaces separati e chiavi API dedicate. | M | Necessaria per isolare gli ambienti (teams, Dev e Prod, infrastruttura). |
| NFR | Data Residency e routing esclusivo all'interno del territorio europeo (EU/EEA). | M | Vincolo fondamentale per la conformità con gli standard interni e i requisiti dei clienti. |
| NFR | Politica di Zero Data Retention (ZDR) contrattualizzata. | M | I prompt e il codice sorgente inviato non devono essere memorizzati né usati per il training. |
| FR | Guardrails economici e Budget Policies con blocchi automatici. | S | Per prevenire picchi di fatturazione o loop incontrollati. |
| FR | Osservabilità dell'utilizzo: metriche su tipo di utilizzo (assistente/agentico), scopo (scrittura codice, PR review, ecc.), modello LLM usato e budget speso. | M | Richiesta del revisore (CTO): serve visibilità sull'uso reale e sull'impatto degli LLM. Coperta dalla dashboard OpenRouter per workspace e dai classificatori di utilizzo configurati. |
| FR | Supporto alla modalità Bring Your Own Key (BYOK). | C | Utile in futuro per tier di prezzo agevolati o crediti diretti con specifici vendor. |

## Peso dei requisiti su base MoSCoW

Pesi adottati: Must = 3, Should = 2, Could = 1 (Won't = 0).

| Requisito | Priorità | Peso | Peso sul totale |
| :---- | :---- | :---- | :---- |
| API Endpoint standardizzato e compatibile con OpenAI SDK. | M | 3 | 16.7% |
| Console di back-office con Workspaces separati e chiavi API dedicate. | M | 3 | 16.7% |
| Data Residency EU/EEA. | M | 3 | 16.7% |
| Zero Data Retention contrattualizzata. | M | 3 | 16.7% |
| Osservabilità dell'utilizzo (metriche su utilizzo, scopo, modello, budget). | M | 3 | 16.7% |
| Guardrails economici e Budget Policies. | S | 2 | 11.1% |
| Bring Your Own Key (BYOK). | C | 1 | 5.6% |

## Valutazione comparativa

Punteggi da 1 (molto scarso) a 5 (ottimo).

| Criterio di Valutazione | Peso | OpenRouter Enterprise | GitHub Copilot | OpenCode Zen | Note / Evidenze |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Fit Funzionale | 30% | 5 | 2 | 4 | OpenRouter supporta 400+ modelli, workspaces separati e budget rigidi. OpenCode Zen offre modelli pre-curati per il coding ma manca della flessibilità di configurazione enterprise di OpenRouter. Copilot è un ambiente utente chiuso. |
| Fit Architetturale | 20% | 5 | 3 | 4 | OpenRouter fornisce un endpoint unico compatibile OpenAI utilizzabile ovunque. OpenCode Zen offre un buon sistema CLI/API pass-through ma con meno opzioni di routing. |
| Security & Compliance | 20% | 5 | 3 | 3 | OpenRouter ha un endpoint EU API con ZDR contrattuale nel DPA e hosting GCP in Europa. OpenCode Zen non offre lo stesso livello di isolamento contrattuale enterprise. |
| Costi (TCO) | 15% | 4 | 4 | 3 | OpenRouter e Zen usano il pay-as-you-go, ma OpenRouter permette l'ottimizzazione automatica tramite l'istruzione `:floor`. Copilot ha costi fissi slegati dall'uso reale. |
| Vendor & Support | 15% | 4 | 4 | 4 | Sia OpenCode sia OpenRouter garantiscono un canale Enterprise diretto. |
| PUNTEGGIO PONDERATO | 100% | 4.75 / 5 | 2.95 / 5 | 3.75 / 5 | OpenRouter Enterprise risulta la scelta più idonea per le esigenze di Madisoft. |

## Analisi finanziaria

Per confrontare l'efficienza economica del sistema a token pass-through, l'analisi prende come riferimento il costo di computazione sul modello Kimi K2.6, calcolato su un volume ipotetico di 1 Milione di token.

- **OpenCode Zen (listino fisso):** read $0.95, write $4.00, cached-read $0.16.
- **OpenRouter Enterprise (provider più economico, es. DeepInfra):** read $0.75 (risparmio del 21% rispetto a Zen), write $3.50 (risparmio del 12%), cached-read $0.15.

Ottimizzazione di budget aziendale: sfruttando il suffisso `:floor` all'interno del model slug, OpenRouter instrada la richiesta sul fornitore momentaneamente più economico (es. DeepInfra o Parasail), garantendo un abbattimento dei costi dinamico rispetto ai prezzi fissi dei competitor. Vedi [introducing nitro and floor price shortcuts](https://openrouter.ai/blog/announcements/introducing-nitro-and-floor-price-shortcuts/#floor-price-prioritize-cost-).

## Analisi Security & Compliance

- **GDPR Compliance:** pienamente soddisfatta. Il DPA include le Clausole Contrattuali Standard (SCC) Modulo 2 (Controller-to-Processor) con giurisdizione e foro di riferimento stabiliti a Dublino, Irlanda.
- **EU Isolation & ZDR:** l'endpoint OpenRouter dedicato alla gestione europea (EU API) garantisce contrattualmente che i payload vengano elaborati esclusivamente all'interno dell'Unione Europea o dello Spazio Economico Europeo (infrastruttura Google Cloud Platform regolata da restrizioni regionali) e che venga applicata la Zero Data Retention immediata al completamento della richiesta.
- **Sicurezza delle informazioni:** il fornitore adotta il framework di controllo SOC 2 Type II, crittografia TLS 1.2+ in transito, AES-256 a riposo e Web Application Firewall (WAF) Cloudflare.
- **Esito verifica interna:** valutazione sicurezza IS-313 chiusa con esito Done; Qualifica Fornitore e DPIA approvata con stato Green (compliant con riserva, vedi Piano di adozione).

## Decisione finale

- **Soluzione scelta:** OpenRouter Enterprise.
- **Motivazione:** lo strumento supera i vincoli e le rigidità di GitHub Copilot. Offre garanzie giuridiche e infrastrutturali eccellenti per il trattamento dei dati in ambito europeo (EU API e ZDR) e un set di strumenti amministrativi (Workspaces e Budgeting) indispensabili per la governance tecnica di Madisoft.
- **Approvazione:** approvata in riunione il 12/10/2026 da CTO (Francesco Trucchia) e CEO (Diego Moretti). Non è prevista una firma formale; l'approvazione è stata data in sede di meeting. Il budget è stato caricato dal CEO sul conto OpenRouter.

## Alternative considerate

- **Mantenimento di GitHub Copilot:** scartata perché troppo rigida; non permette di cambiare istantaneamente il modello sottostante e manca di un back-office avanzato per la segregazione degli ambienti di dev/test.
- **Integrazione con OpenCode Zen:** provider dalle caratteristiche simili a OpenRouter; il back-office è meno maturo e non offre modelli con EU Residency.
- **Integrazione diretta con le API dei singoli vendor (OpenAI, Anthropic):** scartata perché comporterebbe un effort di manutenzione elevato delle chiavi e del codice di integrazione, oltre al rischio di frammentazione del fatturato.

## Temi aperti dai commenti di revisione

- **Osservabilità dell'utilizzo (CTO):** recepita come requisito funzionale (vedi sezione Requisiti); coperta dalla dashboard OpenRouter e dai classificatori di utilizzo già sperimentati.
- **Review automatica delle PR di GitHub Copilot (CTO):** oggi vari dev usano la funzione di review automatica integrata in GitHub. Va deciso se mantenerla in parallelo a OpenRouter. OpenRouter non offre una review automatica nativa, ma il [Report finale](report-finale-openrouter.md) documenta un esperimento interno di PR review agentica tramite API (es. Kimi 3), con esito positivo su PR corpose. Da valutare in fase di onboarding come tooling esterno o interno.

## Piano di adozione

- **Timeline di onboarding:** 1-2 mesi di sandbox controllata (Ferdinando e 3/4 dev) con investimento iniziale controllato di 200$ totali.
- **Metriche di successo:** incremento della velocità di delivery sui refactoring complessi e mantenimento della spesa entro la soglia storica dei 20$/mese per utente una volta eseguito il rollout definitivo.
- **Owner responsabile:** Ferdinando Santacroce.
- **Condizione di compliance:** routing EU-only e Zero Data Retention confermati (riunione del 12/10/2026); il piano Business si sottoscrive con tali garanzie, responsabile Pasquale Siciliano.
- **Prosecuzione approvata:** il piano operativo di introduzione (budget, configurazione, roll out e formazione, misurazione) è in [Piano di rollout: adozione OpenRouter](piano-rollout-openrouter.md); l'avvio operativo parte con il kickoff del 13/10/2026.

## Tracciamento Jira

Le attività dell'iniziativa OpenRouter sono tracciate nel progetto **STAFF** (Team Staff+):

- [STAFF-118](https://madisoft.atlassian.net/browse/STAFF-118) - OpenRouter: adozione come AI gateway aziendale (Epica contenitore).
- [STAFF-119](https://madisoft.atlassian.net/browse/STAFF-119) - ricerca informazioni e materiale di valutazione.
- [STAFF-120](https://madisoft.atlassian.net/browse/STAFF-120) - creazione del pitch di adozione.
- [STAFF-121](https://madisoft.atlassian.net/browse/STAFF-121) - presentazione del pitch a CEO e CTO.
- [STAFF-122](https://madisoft.atlassian.net/browse/STAFF-122) - sperimentazione con il gruppo di sviluppo.
- [STAFF-105](https://madisoft.atlassian.net/browse/STAFF-105) - redazione del report finale di sperimentazione.
- [STAFF-123](https://madisoft.atlassian.net/browse/STAFF-123) - approvazione del piano di adozione.
- [STAFF-124](https://madisoft.atlassian.net/browse/STAFF-124) - piano di rollout.
- [STAFF-125](https://madisoft.atlassian.net/browse/STAFF-125) - linea guida server MCP locali e richiesta [IS-395](https://madisoft.atlassian.net/browse/IS-395).
