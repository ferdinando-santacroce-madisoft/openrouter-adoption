# Sintesi canale Slack #prj-openrouter (14/07 → 09/09/2026)

Fonte: timeline_full.md (205 messaggi top + 749 replies). Autori:
Ferdinando (Owner), Davide Fossacecchi, Federico Bartoli, Francesco Trucchia (CTO), Anders Jipwouo, Massimiliano Conforti, Lorenzo Piersante, Marco Martorana, Pasquale Siciliano (IT-Security).

## Timeline chiave
- 14/07: canale creato, inviti su OpenRouter. Subito scherzo "ho già speso 5000$". Ferdinando: "dobbiamo darci obiettivi misurabili". Nando setta workspace e guardrail.
- 14/07: ap. key di Davide senza guardrail settimanale; Nando lo aggiunge. Scoperta: i guardrail si ereditano a livello utente/workspace ma non si vedono sull'API key.
- 15/07: primo test DS4 Flash: 6% di contesto usato in planning, "meno greedy di contesto", 6 cents. Confronti: DS4 Flash ~ Sonnet, GLM 5.2 ~ Opus. Invito Miro.
- 16/07: errore `Corrupted thought signature` (Lorenzo, modelli Google). Il classificatore rifiuta dati "sensibili". Incidente Google 3.1 Pro → passaggio a 3 Flash. Visto nei log.
- 17/07: Kimi 3 linkato (equivalente "Fable 5"/"GPT 5.6" a 1/3). Lorenzo: budget settimanale finito, consiglio DS4 Pro = 15 cent per un pomeriggio. Federico prova Kimi 3 (30 cents), "vai a casa umano".
- 20/07: scoperto che OpenCode usa "Nano Banana 2" per generare titoli di sessione → consumi non voluti. Tema small_model.
- 21/07: richiesta metrriche del CTO (4 punti: tipo utilizzo, scopo, tipologia LLM, budget). Davide propone workspace-per-team. Trucchia: l'unità minima è il team. Deep dive su: prompt = conoscenza aziendale, review su GitHub non nativa, log dei prompt.
- 22/07: discussioni su "comandi" di OpenCode = macro. Refinement del concetto "conoscenza condivisa".
- 28/07: incidente budget: Trucchia brucia 6$ in 2 giorni in ferie. Esperimento CTO: plan mode estrazione modulo Comunicazioni (piano a barra verde) → "sulla carta sensato", da iterare con multipli Plan. Tema SDLC.
- 29/07: CTO disabilita chiavi di Marco nel Default Workspace (senza policy), le sposta in madisoft-test (policy 6$/sett). Marco aveva speso 23$ (app). Lorenzo: esperimento agentico Interpelli, risparmio 30-40%, ~3$/giorno con DS4 Pro, chiede budget extra.
- 29/07: Davide nota che il routing va messo a posto: DS4 Flash "rincoglionito", quantizzazione variabile per provider, token/s variabili.
- 30/07: Pasquale recap policy AI di gruppo: uso AI senza licenza enterprise vietato per codice/segreti; MCP locali ok (da formalizzare); Gemini ok se licenza cloud. Discussione NIS2/logging, sandboxing agenti. Davide spiega l'architettura harness→modelli.
- 05/08: Pasquale pubblica IS-313 + Qualifica Fornitore e DPIA OpenRouter Enterprise → compliant (con riserva) con direttive obbligatorie: Data Residency EU, prevenzione leak (.gitignore/.cbmignore), ZDR. Federico nota che col routing EU "inutilizzabile" (pochi modelli EU). Nando scrive per attivare routing EU esclusivo (solo Enterprise).
- 05/08: Davide propone i Classifier (beta) per taggare generazioni. Nando: "ci smanettiamo domani".
- 06/08: prime metriche classifier (autonomy_level ispirato ad Addy Osmani). Le generazioni, non i prompt, solo in ingresso. Dibattito logging prompt (knowledge aziendale vs privacy/art.4) — Trucchia, Lorenzo (rischi), Federico (comportamento "in posa", shadow AI), Pasquale (logging obbligo NIS2), Davide (costo sociale). Nando: oggi mob programming 2h con AI.
- 12/08: Davide segnala classificatore Autonomy troppo ottimistico (L3 vs L2). Aggiornato il 17/08.
- 19/08: Davide: "dobbiamo avere AI Champion di team e una Cop AI"; serve piano strutturato di adozione.
- 21/08: esperimento vibe coding DS4 Flash free: app React da PDF in 7 minuti, si è fatto anche giro nel browser.
- 24/08: esperimento Davide: aprire PR all'agente e fargli la review → punto di feedback stabile. Lorenzo: subagent usano Gemini 3.5 Flash Light; per i titoli serve small_model; il classificatore è lato OpenRouter.
- 25/08: Nando: invito riunione 26/08 per tirare le somme. Nota: costo classificatore > modello selezionato (DS4 Flash).
- 26/08: riunione, chiusura sperimentazione, presentazione risultati. Nando si abbonò a Codex (regalo 20$/mese a OpenAI). Nando e Davide sviluppano 2 issue Prometeo con AI senza toccare codice (pair+AI). SI pianifica gilda TCPDF. Federico: filtro su article "AI coding will prevent expertise".
- 28/08: Nando si è freezato Meet, riavvia PC (umorismo).
- 31/08: Massimiliano: errore "credits exceeded"; Nando: "abbiamo finito i soldi, venerdì avanzavano 3$".
- 09/09: chiacchiere finali (artisanal software society), niente dati.

## Costi osservati (da canale)
- DS4 Flash: 6 cents (primo test, 15/07); ~0,06$/sessione.
- DS4 Pro: 0,15$ un pomeriggio intero (Lorenzo 17/07).
- Kimi 3: 30 cents (Federico 17/07); ~0,30$.
- Sonnet 4.5: 2$ per "un task del cazzo" (Davide 03/08) → non conveniente.
- Lorenzo: ~3$/giornata con DS4 Pro (29/07).
- Trucchia: 6$ in 2 giorni in ferie (28/07).
- Marco: 23$ + incidente 40$ in 2 giorni con GPT Sol via auto-router (chiave nel workspace sbagliato, 28-29/07).
- CTO (28/07): 30% consumato in 2 giorni di sola IA (con DS4 Flash).
- Budget trial 200$; 31/08 finiti i crediti (ultimo venerdì avanzavano 3$). Guardrail workspace madisoft-test: 6$/settimana. Default Workspace screenshot: $6/weekly ma "No policy" per CTO (il 29/07) — discrepanza da verificare.
- Router: modello di classificazione usa Gemini (non selezionabile liberamente).

## Citazioni chiave (selezionate)
- "Il prompt è conoscenza aziendale. Scrivere software è uno sport di gruppo, non individuale." — Francesco Trucchia
- "Se il prompt genera il codice, il prompt è conoscenza aziendale." — Francesco Trucchia
- "L'unità minima di valore è il team, la maggior parte dei tool è fortemente individualista." — Francesco Trucchia
- "Se so che è attribuibile e leggibile, scrivo prompt presentabili invece che efficaci. Nel caso peggiore qualcuno apre ChatGPT sul telefono: shadow AI." — Federico Bartoli
- "Il logging è un obbligo, non un'opzione. Come soggetto NIS2 essenziale dobbiamo garantire la tracciabilità." — Pasquale Siciliano
- "Secondo me il classificatore sul livello di autonomia che abbiamo creato è troppo ottimistico." — Davide Fossacecchi
- "Ho fatto una roba con Sonnet 4.5... NON L'AVESSI MAI FATTO. Ci pagavo Kimi con quei soldi e mi davano anche il resto." — Davide Fossacecchi
- "mi sa che c'è un bug sul prezzo del budget: vedo 6 euro al posto di 600 euro" — Massimiliano Conforti
- "Si sboccia!" — Ferdinando Santacroce (incidente 40$)
- "vai a casa umano" — Kimi 3 (riportato da Federico)
- "Dobbiamo avere AI Champion di team e una Cop AI." — Davide Fossacecchi
- "Sto gruppo di test e queste conversazioni sono per me Food for Thought." — Francesco Trucchia
- "Io uso parecchio Copilot per le sole review, per tutti gli altri utilizzi dura troppo poco." — Lorenzo Piersante
- "Che mi sembrano meno greedy di contesto quindi rispondono prima e costano meno." — Davide (DS4 Flash)

## Note/decisioni
- Strategia workspace per team (unità minima = team) + chiavi API dedicate.
- Guardrail: 3 livelli Organization→Workspace→User; meglio a livello workspace.
- Default Workspace: da poter bloccare a zero (no guardrail associati). Incidente 40$ → lezione.
- Auto-router: da usare con cautela / policy (white-list/black-list) perché ha scelto GPT Sol (costoso).
- Logging prompt: tema aperto tra NIS2 (obbligo tracciabilità, Pasquale), privacy/art.4 (Lorenzo), comportamento "in posa"/shadow AI (Federico), costo sociale (Davide). Aggregati per team ok; individuale no. Decisione da formalizzare.
- Classifier: ispirato ad Addy Osmani (L0-L5); taggano le generazioni (non i prompt), solo in ingresso. Autonomy ottimistico → aggiornato 17/08.
- Sandboxing agenti: valutazione futura (Docker/Kiro). Nessuno lo fa.
- I/O logging OpenRouter: non applicabile all'endpoint EU (vincolo). Possibilità di inviare log esternamente (AWS/SIEM) da valutare.
- Integrazione Swarmia: non nativa per OpenRouter; API custom (CUSTOM AI TOOL INTEGRATIONS) possibile, ma agganciata all'harness (servirebbe harness unica).
- Modelli testati: DeepSeek V4 Flash (preferito), V4 Pro, GLM 5.2, Kimi 3 (forte FE/review), Sonnet 4.5 (no), Gemini 3.5 Flash Light (subagent default).
- Esperimento CTO plan mode (modulo Comunicazioni): piano sensato "sulla carta", da iterare.
- Pratica di successo: pair/mob programming con l'AI (2 issue Prometeo senza toccare codice; navigation).
- Esperimento PR agentica di Davide (24/08): aprire PR e fargli la review, dare feedback in un punto.
