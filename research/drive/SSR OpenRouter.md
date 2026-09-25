Pitch: [Adozione OpenRouter](https://docs.google.com/document/d/1cJzlOBfJdFqVby6GiRHPNTsg2NwZghfOv2pwXwBHjxI/edit?tab=t.0)

# **SSR: adozione OpenRouter**

## **Informazioni di base**

* **Titolo selezione:** Adozione OpenRouter Enterprise come gateway unificato LLM per l'ingegneria del software  
* **Proposer:** Ferdinando Santacroce  
* **Data:** 10/07/2026  
* **Business need:** Centralizzare l'accesso ai modelli di Intelligenza Artificiale per i team di sviluppo, garantendo l'intercambiabilità dei modelli (evitando il vendor lock-in), il controllo granulare delle spese per ambiente e il rispetto delle normative europee sul trattamento dei dati (GDPR).

## **Requisiti (Matrice MoSCoW)**

| Tipo | Requisito | Priorità | Note |
| :---- | :---- | :---- | :---- |
| **FR** | API Endpoint standardizzato e compatibile con OpenAI SDK. | **M** | Essenziale per un innesto agile nei tool di sviluppo. |
| **FR** | Console di back-office con Workspaces separati e chiavi API dedicate. | **M** | Necessaria per isolare gli ambienti (ambienti diversi per team, per Dev e Prod se usassimo l’AI nei nostri progetti software, in infrastruttura, etc.) |
| **NFR** | Data Residency e routing esclusivo all'interno del territorio europeo (EU/EEA). | **M** | Vincolo fondamentale per la conformità con i nostri standard interni e requisiti dei clienti. |
| **NFR** | Politica di Zero Data Retention (ZDR) contrattualizzata. | **M** | I prompt e il codice sorgente inviato non devono essere memorizzati o usati per il training. |
| **FR** | Guardrails economici e Budget Policies con blocchi automatici. | **S** | Per prevenire picchi di fatturazione o loop incontrollati. |
| **FR** | Supporto alla modalità Bring Your Own Key (BYOK). | **C** | Utile se in futuro avremo tier di prezzo agevolati o crediti diretti con specifici vendor. |

## **Valutazione Comparativa (Scoring Matrix)**

*Punteggi da 1 (molto scarso) a 5 (ottimo).*

| Criterio di Valutazione | Peso | OpenRouter Enterprise | GitHub Copilot | OpenCodeZen | Note / Evidenze |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Fit Funzionale** | 30% | **5** | **2** | **4** | OpenRouter supporta 400+ modelli, workspaces separati e budget rigidi. OpenCode Zen offre modelli pre-curati per il coding ma manca della flessibilità di configurazione enterprise di OpenRouter. Copilot è un ambiente utente chiuso. |
| **Fit Architetturale** | 20% | **5** | **3** | **4** | OpenRouter fornisce un endpoint unico compatibile OpenAI utilizzabile ovunque. OpenCode Zen offre un buon sistema CLI/API pass-through ma con meno opzioni di routing. |
| **Security & Compliance** | 20% | **5** | **3** | **3** | OpenRouter ha un endpoint specifico EU API con ZDR contrattuale nel DPA e hosting GCP in Europa. OpenCode Zen non offre lo stesso livello di isolamento contrattuale enterprise (DPA strutturato per l'Europa). |
| **Costi (TCO)** | 15% | **4** | **4** | **3** | OpenRouter e Zen usano il pay-as-you-go, ma OpenRouter permette l'ottimizzazione automatica tramite l'istruzione :floor. Copilot ha costi fissi slegati dall'uso reale. |
| **Vendor & Support** | 15% | **4** | **4** | **4** | Sia OpenCode che OpenRouter garantiscono un canale Enterprise diretto. |
| **PUNTEGGIO PONDERATO** | **100%** | **4.75 / 5** | **2.95 / 5** | **3.75 / 5** | **OpenRouter Enterprise risulta la scelta più idonea per le esigenze di Madisoft.** |

## **3\. Analisi Finanziaria e Benchmark (Scenario Reale)**

Per confrontare l'efficienza economica del sistema a token pass-through, l'analisi prende come riferimento il costo di computazione sul modello *Kimi K2.6* (calcolato su un volume ipotetico di 1 Milione di token):

* **OpenCode Zen (Listino Fisso):**  
  * Read: $0.95  
  * Write: $4.00  
  * Cached-Read: $0.16  
* **OpenRouter Enterprise (Tramite il provider più economico, es. DeepInfra):**  
  * Read: **$0.75** (Risparmio del 21% rispetto a Zen)  
  * Write: **$3.50** (Risparmio del 12% rispetto a Zen)  
  * Cached-Read: **$0.15**

📌 **Ottimizzazione di Budget Aziendale:** [sfruttando il suffisso “:floor” all'interno dei model slug](https://openrouter.ai/blog/announcements/introducing-nitro-and-floor-price-shortcuts/#floor-price-prioritize-cost-), OpenRouter instrada la richiesta sul fornitore momentaneamente più economico (es. DeepInfra o Parasail), garantendo un abbattimento dei costi dinamico rispetto ai prezzi fissi dei competitor.

## **Analisi Security & Compliance (Sintesi DPA)**

* **GDPR Compliance:** Pienamente soddisfatta. Il DPA include le Clausole Contrattuali Standard (SCC) Modulo 2 (Controller-to-Processor) con giurisdizione e foro di riferimento stabiliti a Dublino, Irlanda.  
* **EU Isolation & ZDR:** L'endpoint OpenRouter dedicato alla gestione europea (EU API) garantisce contrattualmente che i payload vengano elaborati esclusivamente all'interno dell'Unione Europea o dello Spazio Economico Europeo (infrastruttura Google Cloud Platform regolata da restrizioni regionali) e che venga applicata la *Zero Data Retention* immediata al completamento della richiesta.  
* **Sicurezza delle Informazioni:** Il fornitore adotta il framework di controllo **SOC 2 Type II**, crittografia TLS 1.2+ in transito, AES-256 a riposo e Web Application Firewall (WAF) Cloudflare.

## **Decisione finale**

* **Soluzione scelta:** OpenRouter Enterprise  
* **Motivazione:** Lo strumento supera i vincoli e le rigidità di GitHub Copilot. Offre garanzie giuridiche e infrastrutturali eccellenti per il trattamento dei dati in ambito europeo (EU API \+ ZDR) e un set di strumenti amministrativi (Workspaces e Budgeting) indispensabili per la governance tecnica di Madisoft.  
* **Approvazione Board:** \[DA COMPLETARE: Data e Firme CEO, CTO, IT\&CyberSecurity\]

## **Piano di adozione & Monitoraggio**

* **Timeline di onboarding:** 1-2 mesi di Sandbox controllata (Ferdinando \+ 3/4 dev) con investimento iniziale controllato di 200$ totali.  
* **Metriche di successo:** Incremento della velocità di delivery sui refactoring complessi e mantenimento della spesa entro la soglia storica dei 20$/mese per utente una volta eseguito il rollout definitivo.  
* **Owner responsabile:** Ferdinando Santacroce

