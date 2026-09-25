#!/usr/bin/env python3
"""Builds Google Slides batchUpdate JSON payloads for the OpenRouter adoption deck.
Layout: 16:9 (9144000 x 5143500 EMU). BLANK layout id: p12."""
import json, os, sys

EMU = 12700
W, H = 9144000, 5143500
MARG = int(0.5 * 72 * EMU)   # 0.5 inch margin
CW = W - 2 * MARG            # content width
OUT = "/tmp/opencode/batches"
os.makedirs(OUT, exist_ok=True)

ACCENT = {"red": 0.043, "green": 0.337, "blue": 0.816}   # #0B57D0
DARK = {"red": 0.10, "green": 0.10, "blue": 0.10}
GRAY = {"red": 0.35, "green": 0.35, "blue": 0.35}

def pt(v): return int(v * 72 * EMU)

def rect_req(oid, page, x, y, w, h, color):
    create = {"createShape": {
        "objectId": oid, "shapeType": "RECTANGLE",
        "elementProperties": {
            "pageObjectId": page,
            "size": {"width": {"magnitude": w, "unit": "EMU"}, "height": {"magnitude": h, "unit": "EMU"}},
            "transform": {"scaleX": 1, "scaleY": 1, "translateX": x, "translateY": y, "unit": "EMU"}}}}
    update = {"updateShapeProperties": {
        "objectId": oid,
        "fields": "shapeBackgroundFill.solidFill.color,outline.outlineFill.solidFill.color",
        "shapeProperties": {"shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": color}}},
                            "outline": {"outlineFill": {"solidFill": {"color": {"rgbColor": color}}}}}}}
    return [create, update]

def txt_req(oid, page, x, y, w, h):
    return {"createShape": {
        "objectId": oid, "shapeType": "TEXT_BOX",
        "elementProperties": {
            "pageObjectId": page,
            "size": {"width": {"magnitude": w, "unit": "EMU"}, "height": {"magnitude": h, "unit": "EMU"}},
            "transform": {"scaleX": 1, "scaleY": 1, "translateX": x, "translateY": y, "unit": "EMU"}}}}

def ins_req(oid, text):
    return {"insertText": {"objectId": oid, "text": text}}

def style_req(oid, size_pt, bold=False, color=None, italic=False):
    style = {"fontSize": {"magnitude": size_pt, "unit": "PT"}, "bold": bold}
    if color is not None:
        style["foregroundColor"] = {"opaqueColor": {"rgbColor": color}}
    if italic:
        style["italic"] = True
    return {"updateTextStyle": {"objectId": oid, "style": style,
                                "fields": ",".join(["fontSize","bold","italic"] if italic else ["fontSize","bold"]) + (",foregroundColor" if color else ""),
                                "textRange": {"type": "ALL"}}}

def title_block(page, idx, title, accent_line=True):
    oid = f"title{idx}"
    reqs = []
    # title text
    reqs.append(txt_req(oid, page, MARG, int(0.35*72*EMU), CW, pt(0.9)))
    reqs.append(ins_req(oid, title))
    reqs.append(style_req(oid, 27, bold=True, color=DARK))
    if accent_line:
        reqs += rect_req(f"line{idx}", page, MARG, int(1.15*72*EMU), CW, int(0.045*72*EMU), ACCENT)
    return reqs

def body_block(page, idx, lines, start_pt=1.5, size=15.5, gap_pt=0.42):
    oid = f"body{idx}"
    reqs = []
    y = int(start_pt*72*EMU)
    reqs.append(txt_req(oid, page, MARG, y, CW, H - y - MARG))
    # lines: list of (text, level) level 0 bullet, 1 sub-indent
    blocks = []
    for it in lines:
        text, lvl = it
        prefix = "•  " if lvl == 0 else "    –  "
        blocks.append(prefix + text)
    reqs.append(ins_req(oid, "\n".join(blocks)))
    # style: set all to 15.5; then enlarge first line lead if marked
    reqs.append(style_req(oid, size, color=DARK))
    return reqs

def kpi_block(page, idx, kpis, start_pt=1.9):
    """kpis: list of (number, label). Renders big-number boxes 2x2."""
    reqs = []
    cols, rows = 2, (len(kpis)+1)//2
    bxw = (CW - pt(0.5)) // cols
    bxh = int((H - start_pt*72*EMU - 2*MARG) / rows) if rows else 0
    for i, (num, lab) in enumerate(kpis):
        r, c = divmod(i, cols)
        x = MARG + c*(bxw + pt(0.5))
        y = int(start_pt*72*EMU) + r*bxh
        # background soft panel
        reqs += rect_req(f"kbg{idx}_{i}", page, x, y, bxw-pt(0.3), bxh-pt(0.3),
                         {"red": 0.95, "green": 0.97, "blue": 1.0})
        nid = f"knum{idx}_{i}"
        lid = f"klab{idx}_{i}"
        # number
        reqs.append(txt_req(nid, page, x+pt(0.35), y+pt(0.25), bxw-pt(0.7), pt(0.9)))
        reqs.append(ins_req(nid, num))
        reqs.append(style_req(nid, 30, bold=True, color=ACCENT))
        # label
        reqs.append(txt_req(lid, page, x+pt(0.35), y+bxh-pt(0.65), bxw-pt(0.7), pt(0.5)))
        reqs.append(ins_req(lid, lab))
        reqs.append(style_req(lid, 12.5, color=GRAY))
    return reqs

def slide(page, idx, title, builder, *args):
    reqs = [{"createSlide": {"objectId": page, "insertionIndex": idx-1,
                             "slideLayoutReference": {"layoutId": "p12"}}}]
    reqs += title_block(page, idx, title)
    reqs += builder(page, idx, *args)
    return reqs

def make_slide(n, title, lines, start_pt=1.5, size=15.5):
    return slide(f"slide{n:02d}", n, title, body_block, lines, start_pt, size)

def make_kpi(n, title, kpis):
    return slide(f"slide{n:02d}", n, title, kpi_block, kpis)

deck = {}

# S1 copertina: uses existing title slide (i0 CENTERED_TITLE, i1 SUBTITLE)
deck["01_cover"] = {
    "requests": [
        ins_req("i0", "OpenRouter come AI Gateway aziendale"),
        {"updateTextStyle": {"objectId": "i0",
                             "style": {"bold": True, "fontSize": {"magnitude": 40, "unit": "PT"}},
                             "fields": "bold,fontSize", "textRange": {"type": "ALL"}}},
        ins_req("i1", "Risultati della sperimentazione e proposta di adozione\nLuglio – Settembre 2026  ·  Ferdinando Santacroce  ·  Madisoft"),
        {"updateTextStyle": {"objectId": "i1",
                             "style": {"fontSize": {"magnitude": 18, "unit": "PT"}},
                             "fields": "fontSize", "textRange": {"type": "ALL"}}},
    ]
}

# S2
deck["02_exec"] = make_slide(2, "Executive summary", [
    ("La sperimentazione ha validato OpenRouter su lavoro reale: issue di produzione, non demo.", 0),
    ("Riduzione dei tempi fino a -60% (test) e PR complete a 0,66€.", 0),
    ("Spesa controllata: $199,76 su un budget trial di $200.", 0),
    ("Compliance: DPIA e Qualifica Fornitore approvate (Green); Zero Data Retention attivo.", 0),
    ("Routing EU disponibile con il piano Business: 71 modelli su 625, inclusi i principali.", 0),
    ("Richiesta: via libera al passaggio al piano Business e al rollout.", 0),
])

# S3
deck["03_cosa"] = make_slide(3, "Cosa abbiamo fatto", [
    ("6 sviluppatori + il CTO · dal 14/07 al 09/09/2026.", 0),
    ("11 issue di produzione completate e chiuse su Jira, con metriche.", 0),
    ("Harness principale OpenCode → OpenRouter; modelli DeepSeek V4, Kimi, GLM, Sonnet.", 0),
    ("Metriche automatiche: classificatori sul gateway (autonomy level, work type).", 0),
    ("Governance: workspace dedicati, chiavi API per persona, guardrails economici.", 0),
])

# S4
deck["04_numeri"] = make_kpi(4, "I numeri in sintesi", [
    ("$199,76", "spesa totale su $200 di budget trial"),
    ("22K", "richieste gestite"),
    ("876M", "token totali · 76,5% da cache"),
    ("$0,23", "costo per 1M token (blended)"),
])

# S5
deck["05_tempi"] = make_slide(5, "Riduzione dei tempi (casi reali)", [
    ("Scrittura test: -60% (PRO-1128).", 0),
    ("PR da 402 righe in 1h45m contro 4h20m a mano (PRO-1190).", 0),
    ("Frontend mai visto prima: PR in 1h senza onboarding (PRO-1272).", 0),
    ("Diagnosi di test falliti in meno di 3 minuti (PRO-1327).", 0),
    ("1.700 righe di test in 10 ore, 13 classi coperte (PRO-1271).", 0),
    ("33% di un'epica consegnato in un giorno (PRO-1249).", 0),
])

# S6
deck["06_costi"] = make_slide(6, "Costi per task: il confronto che conta", [
    ("OpenRouter: PR completa a 0,66€ (PRO-1190); sessione quotidiana ~0,06$ con DeepSeek V4 Flash.", 0),
    ("GitHub Copilot: abbonamento a plafond che si esaurisce a metà giornata di lavoro agentico.", 0),
    ("Modello pay-as-you-go: si paga solo l'uso reale, nessun tetto che si satura.", 0),
    ("Costo medio osservato ~22$/dev/mese, in linea col tetto target di 20$.", 0),
])

# S7
deck["07_flessibilita"] = make_slide(7, "Flessibilità e anti lock-in", [
    ("Accesso a 400+ modelli, inclusi gli Open Weights di frontiera.", 0),
    ("71 modelli anche in regione EU, inclusi DeepSeek V4 Flash, GLM, Kimi, Sonnet, Gemini Flash Lite.", 0),
    ("Il modello giusto per ogni task: DeepSeek V4 Flash (quotidiano), Kimi (FE e review), GLM 5.2 (analisi).", 0),
    ("Cambio di modello immediato: se un provider peggiora o rincara, si passa ad altro senza migrazione.", 0),
    ("Riduce il rischio di vincolo a un vendor (anche vs Claude/Codex: modelli chiusi e più costosi).", 0),
])

# S8
deck["08_governance"] = make_slide(8, "Governance e controllo costi", [
    ("Guardrails economici per workspace con blocco automatico (es. 6$/settimana).", 0),
    ("Chiavi API dedicate per persona/team: consumi attribuibili.", 0),
    ("Dashboard di utilizzo per team — l'unità minima richiesta dal CTO.", 0),
    ("Incidente governato: 40$ in 2 giorni per una chiave nel workspace sbagliato → workspace di default bloccato a zero.", 0),
])

# S9
deck["09_osservabilita"] = make_slide(9, "Osservabilità con i classificatori", [
    ("Autonomy Level (L0–L5): 58% L2, 24% L3 → uso prevalentemente agentico su task delimitati.", 0),
    ("Work type: feature 29%, refactoring 24%, bug fixing 23%, test 8%.", 0),
    ("Tool loop: ~80% delle sessioni in read → write → execute.", 0),
    ("Misura il tipo di utilizzo senza leggere i prompt (privacy preservata).", 0),
    ("Integrazione con Swarmia: possibile via API custom, in follow-up.", 0),
])

# S10
deck["10_sicurezza"] = make_slide(10, "Sicurezza e compliance", [
    ("IS-313 — Valutazione sicurezza OpenRouter Enterprise: completata (Done).", 0),
    ("DPIA / Qualifica Fornitore OpenRouter Enterprise: approvata, stato Green (05/08/2026).", 0),
    ("Zero Data Retention contrattuale: attivo sui modelli utilizzati.", 0),
    ("Routing esclusivo EU: disponibile con il piano Business (71 modelli EU su 625, inclusi i nostri).", 0),
    ("NIS2: tracciabilità garantita senza log EU; prevenzione leak via .gitignore/.cbmignore.", 0),
])

# S11
deck["11_criticita"] = make_slide(11, "Criticità e trasparenza", [
    ("Qualità dei provider non omogenea sullo stesso modello (reattività variabile).", 0),
    ("Guardrails efficaci solo se configurati sul workspace giusto: incidente 40$, ora mitigato.", 0),
    ("Auto-router da usare con policy: ha selezionato GPT-5.6 Sol, il modello più costoso.", 0),
    ("Repo molto grandi (Nuvola, ~15K file) pesano sui consumi: serve un buon contesto.", 0),
    ("Catalogo EU ristretto (71 su 625): manca DeepSeek V4 Pro, presenti i modelli principali.", 0),
    ("Classificatore di autonomia tende a sovrastimare: in iterazione, dato dichiarato.", 0),
])

# S12
deck["12_piano"] = make_slide(12, "Piano di adozione e richiesta", [
    ("Approvazione → passaggio al piano Business di OpenRouter (routing EU-only e ZDR confermati con IT-Security, firma con il CEO).", 0),
    ("Rollout: workspace per team, onboarding sviluppatori, metriche continue.", 0),
    ("Budget: ~20$/mese per sviluppatore, spostato da Copilot verso OpenRouter.", 0),
    ("Checkpoint mensile su costi e metriche dei classificatori.", 0),
    ("Grazie — spazio alle domande.", 1),
])

for name, payload in deck.items():
    if isinstance(payload, list):
        payload = {"requests": payload}
    with open(f"{OUT}/{name}.json", "w") as f:
        json.dump(payload, f)
    print("wrote", name)
print("done")
