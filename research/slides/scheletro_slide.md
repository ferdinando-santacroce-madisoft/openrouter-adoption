# Scheletro presentazione — "OpenRouter: risultati sperimentazione e proposta di adozione"

Obiettivo: convincere CTO e CEO. ~12 slide, semplici e funzionali.

## Contenuto slide

1. **Titolo** — OpenRouter come AI Gateway aziendale
   Sottotitolo: Risultati della sperimentazione (lug–set 2026) e proposta di adozione · Ferdinando Santacroce

2. **Executive summary** (TL;DR)
   - La sperimentazione ha validato OpenRouter nei flussi di sviluppo reali
   - Riduzione tempi fino a -60% sui test; PR complete a 0,66€
   - Spesa controllata: $199,76 su un budget trial di $200, sotto il tetto di 20$/dev/mese
   - Compliance: IS-313 + DPIA approvata (Green); Zero Data Retention operativo
   - Routing EU: disponibile con il piano Business (71 modelli su 625, inclusi i principali)
   - Richiesta: via libera al passaggio al piano Business e al rollout

3. **Cosa abbiamo fatto**
   - 6 sviluppatori + CTO, 14/07 → 09/09/2026, lavoro reale (issue di produzione, non demo)
   - Harness: OpenCode + modelli DeepSeek V4, Kimi, GLM su OpenRouter
   - Metriche misurate con classificatori automatici sul gateway
   - Governance: workspace dedicati, chiavi, guardrails economici

4. **Numeri chiave**
   - Spesa totale: $199,76 / $200 di budget trial
   - 22K richieste · 876M token · cache hit 76,5%
   - Costo medio: ~$0,23 per 1M token (blended)
   - ~22$/dev/mese (inclusi classificatore e un incidente, al netto ≈ tetto 20$)

5. **Riduzione dei tempi (casi reali, verificati su Jira)**
   - Test: -60% (PRO-1128) · PR 402 righe in 1h45m vs 4h20m (PRO-1190 vs PRO-1156)
   - Frontend mai visto: PR in 1h senza onboarding (PRO-1272)
   - Diagnosi in <3 minuti (PRO-1327) · 33% di un'epica in un giorno (PRO-1249)
   - 1.700 righe di test in 10h (PRO-1271)

6. **Costi per task: il confronto che conta**
   - OpenRouter: 0,66€ una PR completa (PRO-1190) · 0,06$ una sessione DS4 Flash
   - GitHub Copilot: abbonamento a plafond che si esaurisce a metà giornata
   - Modello di consumo: pay-as-you-go, si paga solo l'uso reale

7. **Flessibilità e anti lock-in**
   - 400+ modelli, inclusi gli Open Weights di frontiera
   - 71 modelli anche in regione EU, inclusi DS4 Flash, GLM, Kimi, Sonnet, Gemini Flash Lite
   - Cambio modello per task al volo (DS4 Flash per il quotidiano, Kimi per FE/review, GLM per analisi)
   - Nessun vincolo a un vendor: se un provider peggiora, si cambia modello senza migrazione

8. **Governance e controllo costi**
   - Workspace per team + chiavi API dedicate + guardrails con blocco automatico
   - Classificatori per misurare il tipo di utilizzo (senza leggere i prompt)
   - Lezione appresa: workspace di default a costo zero (incidente 40$ rientrato e risolto)

9. **Classificatori e osservabilità**
   - Autonomy Level (L0–L5): 58% L2 (delega task delimitati), 24% L3 (autonomia condizionata), uso quasi mai puramente assistivo
   - Work type: feature 29%, refactoring 24%, bug fixing 23%, test 8%
   - Dati per team richiesti dal CTO → possibili via workspace + integrazione Swarmia custom (follow-up)

10. **Sicurezza e compliance**
    - IS-313 "Valutazione sicurezza OpenRouter Enterprise": Done
    - DPIA / Qualifica Fornitore OpenRouter Enterprise: approvata (Green), rev 05/08/2026
    - Zero Data Retention contrattuale su modelli selezionati (attivo)
    - Routing esclusivo EU: disponibile con il piano Business (71 modelli EU su 625, inclusi i nostri)
    - Vincoli NIS2/leak gestiti: .gitignore/.cbmignore, no logging EU, sandboxing futura

11. **Criticità e trasparenza**
    - Qualità dei provider non omogenea sullo stesso modello (reattività variabile)
    - Guardrails efficaci solo se sul workspace giusto (incidente 40$ → mitigato)
    - Auto-router da usare con policy (ha selezionato GPT-5.6 Sol, il modello più costoso)
    - Repo molto grandi (Nuvola, 15K file) pesano sui consumi → da ottimizzare contesto
    - Catalogo EU ristretto (71 su 625): manca DeepSeek V4 Pro, presenti i modelli principali

12. **Piano di adozione e richiesta**
    - Se via libera: passaggio al piano Business di OpenRouter (routing EU-only + ZDR confermati con IT-Security, firma con CEO)
    - Rollout: workspace per team, onboarding dev, budget 20$/dev/mese da Copilot verso OpenRouter
    - Checkpoint mensile su costi e metriche classificatori
    - Richiesta: approvazione del piano e dello spostamento del budget
