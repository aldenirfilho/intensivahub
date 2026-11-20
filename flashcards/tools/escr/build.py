#!/usr/bin/env python3
"""Gera o baralho 📜 Escrituras & Axiomas 360X (1000 cards) — .apkg, .csv e índice .md."""
import json
import csv, hashlib, html, importlib, os, re, sys, unicodedata
from collections import Counter, defaultdict
import genanki

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
RAIZ = "📜 Escrituras & Axiomas 360X"
VERSAO = "v1.2 · 16/11/2026"
TOTAL = 1145
CREDITO = "📜 Escrituras & Axiomas 360X · organização e axiomas: Dr. Aldenir Rocha de Oliveira Filho"

TEMAS = {
    "AM": ("💛", "Amor & Compaixão", "#f472b6"),
    "JU": ("⚖️", "Justiça & Ética", "#f59e0b"),
    "SA": ("🧠", "Sabedoria & Conhecimento", "#38bdf8"),
    "CO": ("🛡️", "Coragem & Resiliência", "#ef4444"),
    "FE": ("🙏", "Fé & Transcendência", "#a78bfa"),
    "PZ": ("🕊️", "Paz & Perdão", "#34d399"),
    "FA": ("🏡", "Família & Amizade", "#fb923c"),
    "PR": ("💰", "Prosperidade & Generosidade", "#facc15"),
    "VE": ("🗣️", "Palavra & Verdade", "#22d3ee"),
    "AD": ("🧘", "Autodomínio & Mente", "#818cf8"),
    "TM": ("⏳", "Tempo & Mortalidade", "#94a3b8"),
    "HU": ("🌱", "Humildade & Gratidão", "#4ade80"),
    "SD": ("⚕️", "Saúde & Cuidado", "#2dd4bf"),
    "PA": ("🎯", "Propósito & Ação", "#e879f9"),
    "UN": ("🌍", "Unidade & Humanidade", "#60a5fa"),
}

SURATAS = {1: "Al-Fatiha (A Abertura)", 2: "Al-Baqara (A Vaca)", 3: "Al Imran (A Família de Imran)", 4: "An-Nisa (As Mulheres)",
    5: "Al-Ma’ida (A Mesa Servida)", 6: "Al-An’am (O Gado)", 7: "Al-A’raf (Os Cumes)", 10: "Yunus (Jonas)", 12: "Yusuf (José)",
    13: "Ar-Ra’d (O Trovão)", 14: "Ibrahim (Abraão)", 16: "An-Nahl (As Abelhas)", 17: "Al-Isra (A Viagem Noturna)",
    18: "Al-Kahf (A Caverna)", 20: "Ta-Ha", 21: "Al-Anbiya (Os Profetas)", 23: "Al-Mu’minun (Os Crentes)", 24: "An-Nur (A Luz)",
    25: "Al-Furqan (O Critério)", 26: "Ash-Shu’ara (Os Poetas)", 28: "Al-Qasas (As Narrativas)", 29: "Al-Ankabut (A Aranha)",
    31: "Luqman", 39: "Az-Zumar (Os Grupos)", 40: "Ghafir (O Perdoador)", 41: "Fussilat (Os Detalhados)", 42: "Ash-Shura (A Consulta)",
    46: "Al-Ahqaf (As Dunas)", 49: "Al-Hujurat (Os Aposentos)", 50: "Qaf", 53: "An-Najm (A Estrela)", 55: "Ar-Rahman (O Misericordioso)",
    57: "Al-Hadid (O Ferro)", 59: "Al-Hashr (O Desterro)", 61: "As-Saff (As Fileiras)", 62: "Al-Jumu’a (A Sexta-feira)",
    64: "At-Taghabun (O Engano Mútuo)", 65: "At-Talaq", 67: "Al-Mulk (A Soberania)", 76: "Al-Insan (O Ser Humano)",
    90: "Al-Balad (A Cidade)", 93: "Ad-Duha (A Manhã)", 94: "Ash-Sharh (O Alívio)", 96: "Al-Alaq (O Coágulo)",
    99: "Az-Zalzala (O Terremoto)", 103: "Al-Asr (O Tempo)", 107: "Al-Ma’un (A Pequena Ajuda)", 112: "Al-Ikhlas (A Sinceridade)"}

VAGGAS = [(1, 20, "Yamaka (Pares)"), (21, 32, "Appamāda (Vigilância)"), (33, 43, "Citta (A Mente)"), (44, 59, "Puppha (Flores)"),
    (60, 75, "Bāla (O Tolo)"), (76, 89, "Paṇḍita (O Sábio)"), (90, 99, "Arahanta (O Liberto)"), (100, 115, "Sahassa (Os Milhares)"),
    (116, 128, "Pāpa (O Mal)"), (129, 145, "Daṇḍa (A Violência)"), (146, 156, "Jarā (A Velhice)"), (157, 166, "Atta (O Eu)"),
    (167, 178, "Loka (O Mundo)"), (179, 196, "Buddha (O Desperto)"), (197, 208, "Sukha (A Felicidade)"), (209, 220, "Piya (O Querido)"),
    (221, 234, "Kodha (A Ira)"), (235, 255, "Mala (As Impurezas)"), (256, 272, "Dhammaṭṭha (O Justo)"), (273, 289, "Magga (O Caminho)"),
    (290, 305, "Pakiṇṇaka (Diversos)"), (306, 319, "Niraya (O Inferno)"), (320, 333, "Nāga (O Elefante)"), (334, 359, "Taṇhā (O Desejo)"),
    (360, 382, "Bhikkhu (O Monge)"), (383, 423, "Brāhmaṇa (O Santo)")]

GITA = {2: "Sankhya Yoga (o conhecimento)", 3: "Karma Yoga (a ação)", 5: "Karma Sannyasa Yoga (a renúncia)",
    6: "Dhyana Yoga (a meditação)", 9: "Raja Vidya Yoga (o saber régio)", 11: "Vishvarupa Darshana (a forma universal)",
    12: "Bhakti Yoga (a devoção)", 16: "Daivasura Vibhaga (natureza divina e demoníaca)", 17: "Shraddhatraya Vibhaga (as três fés)"}

LINGUA_NOTA = {
    "hebraico": "Tradução livre do hebraico (numeração de versículos como na Almeida)",
    "grego": "Tradução livre do grego (numeração como na Almeida)",
    "hebraico/aramaico": "Tradução livre do hebraico/aramaico (Avot na numeração da Sefaria)",
    "árabe": "Tradução livre do sentido do árabe (numeração de Kufa)",
    "páli/sânscrito": "Tradução livre do páli/sânscrito",
    "chinês clássico": "Tradução livre do chinês clássico (Analectos: numeração moderna + Legge)",
    "sânscrito": "Tradução livre do sânscrito",
    "grego/latim": "Tradução livre do grego/latim",
    "grego/latim/línguas modernas": "Tradução livre quando o original não é português",
    "várias": "Tradução livre quando o original não é português",
    "—": "Atribuição popular checada contra as fontes",
    "autor": "Texto do catálogo Axiomas 360X, sem alteração",
}

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s or "x"

def parse_ref(ref):
    """Separa obra e capítulo inicial (último token com dígito = localização)."""
    base = re.sub(r"\s*\(.*?\)", "", ref).split(" — ")[0].strip()
    partes = base.rsplit(" ", 1)
    if len(partes) < 2 or not re.search(r"\d", partes[1]):
        return base, None, None
    obra, loc = partes[0].rstrip(" ,·"), partes[1]
    m = re.match(r"^(\d+)(?:[.:](\d+))?", loc)
    if m:
        return obra, int(m.group(1)), (int(m.group(2)) if m.group(2) else None)
    m = re.match(r"^([IVXL]+)\.", loc)
    if m:
        rom = {"I": 1, "V": 5, "X": 10, "L": 50}
        v = 0
        for i, ch in enumerate(m.group(1)):
            n = rom[ch]
            v += -n if i + 1 < len(m.group(1)) and rom[m.group(1)[i + 1]] > n else n
        return obra, v, None
    return obra, None, None

def capitulo_info(num, obra, cap, vers):
    if cap is None:
        return ""
    if num in ("01", "02", "03", "04", "05", "06", "07"):
        return f"{obra}, capítulo {cap}"
    if obra == "Pirkei Avot":
        return f"Pirkei Avot, capítulo {cap} (de 6)"
    if obra == "Alcorão":
        return f"Surata {cap} · {SURATAS.get(cap, '')}".rstrip(" ·")
    if obra == "Dhammapada":
        for a, b, nome in VAGGAS:
            if a <= cap <= b:
                return f"Dhammapada, cap. {VAGGAS.index((a, b, nome)) + 1} · {nome} (versos {a}–{b})"
    if obra == "Bhagavad Gita":
        return f"Bhagavad Gita, cap. {cap} · {GITA.get(cap, '')}".rstrip(" ·")
    if obra == "Analectos":
        return f"Analectos, livro {cap} (de 20)"
    if obra == "Tao Te Ching":
        return f"Tao Te Ching, capítulo {cap} (de 81)"
    if obra.startswith("Marco Aurélio"):
        return f"Meditações, livro {cap} (de 12)"
    if obra.startswith("Sêneca, Cartas"):
        return f"Cartas a Lucílio, carta {cap} (de 124)"
    return ""

def carregar():
    decks = []
    for m in ["d01", "d02", "d03", "d04", "d05", "d06", "d07"]:
        decks += importlib.import_module(m).D
    from ax1 import AX1
    from ax2 import AX2
    linhas_ax = []
    for l in (AX1 + AX2).strip().split("\n"):
        if not l.strip():
            continue
        p = [x.strip() for x in l.split(" | ")]
        if len(p) != 8:
            raise SystemExit("axioma com formato errado: " + l[:60])
        n, tit, eixo, sit, data, tema, enun, com = p
        linhas_ax.append(f"Axiomas 360X · nº {n} — {tit} | {tema} | {enun} | {com} | §{eixo}§{sit}§{data}")
    decks.append(("20", "⚜️ Axiomas 360X — Aldenir Rocha (autor)", "Axiomas 360X · coleção autoral de Aldenir Rocha de Oliveira Filho", "autor", "\n".join(linhas_ax)))
    cards, erros = [], []
    for num, nome, trad, lingua, txt in decks:
        n = 0
        for linha in [l for l in txt.strip().split("\n") if l.strip()]:
            p = [x.strip() for x in linha.split(" | ")]
            if len(p) not in (4, 5):
                erros.append(f"[{num}] formato: {linha[:70]}")
                continue
            ref, tema, msg, licao = p[:4]
            nerd = p[4] if len(p) == 5 else ""
            n += 1
            if num == "19":
                licao = re.sub(r"^Origem real:\s*", "", licao)
            meta = None
            if num == "20":
                _, eixo, sit, data = nerd.split("§")
                meta = dict(eixo=eixo, sit=sit, data=data, n=int(re.search(r"nº (\d+)", ref).group(1)))
                nerd = ""
            selo = "autor" if num == "20" else ("mito" if num == "19" else ("tradicional" if ref.startswith("~") else "canonico"))
            ref = ref.lstrip("~").strip()
            temas = [t.strip() for t in tema.split(",")]
            for t in temas:
                if t not in TEMAS:
                    erros.append(f"[{num}] tema inválido {t}: {ref}")
            for campo, val in (("ref", ref), ("msg", msg), ("licao", licao)):
                if not val:
                    erros.append(f"[{num}] campo vazio {campo}: {linha[:60]}")
            obra, cap, vers = parse_ref(ref)
            cards.append(dict(id=f"ESC-{num}-{n:03d}", num=num, deck=nome, trad=trad, lingua=lingua, ref=ref,
                              tema=temas[0], temas=temas, msg=msg, licao=licao, nerd=nerd, selo=selo,
                              obra=obra, cap=cap, vers=vers, meta=meta,
                              capinfo=(f"Eixo {meta['eixo']} · registrado em {meta['data'][8:10]}/{meta['data'][5:7]}/{meta['data'][:4]}" if meta else capitulo_info(num, obra, cap, vers))))
    return decks, cards, erros

def validar(decks, cards, erros):
    avisos = []
    if len(cards) != TOTAL:
        erros.append(f"TOTAL = {len(cards)} (esperado {TOTAL})")
    por_deck = Counter(c["num"] for c in cards)
    refs = defaultdict(list)
    for c in cards:
        refs[(c["num"], c["ref"])].append(c["id"])
    for k, v in refs.items():
        if len(v) > 1 and k[0] != "19":
            erros.append(f"referência repetida no subbaralho {k}: {v}")
    norm = lambda s: set(re.findall(r"\w{4,}", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode()))
    toks = [(c["id"], norm(c["msg"])) for c in cards]
    for i in range(len(toks)):
        for j in range(i + 1, len(toks)):
            a, b = toks[i][1], toks[j][1]
            if a and b:
                jac = len(a & b) / len(a | b)
                if jac >= 0.55:
                    avisos.append(f"mensagens parecidas ({jac:.2f}): {toks[i][0]} × {toks[j][0]}")
    for c in cards:
        if len(c["msg"]) > 420:
            avisos.append(f"mensagem longa ({len(c['msg'])}): {c['id']} {c['ref']}")
    return por_deck, avisos

CSS = """
.card{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:19px;line-height:1.5;
 color:#e8e6df;background:#0b0f16;text-align:left;padding:0;margin:0}
.cx{max-width:720px;margin:14px auto;padding:20px 22px 18px;border-radius:16px;
 background:radial-gradient(120% 140% at 0% 0%,#1a2230 0%,#0f141d 55%,#0b0f16 100%);
 border:1px solid #3b3220;box-shadow:0 0 0 1px #0e7490 inset,0 8px 28px rgba(0,0,0,.45)}
.top{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.chip{display:inline-block;font-size:.72em;font-weight:600;padding:3px 10px;border-radius:999px;
 border:1px solid #4b3d1f;background:#141a24;color:#e7c66a;letter-spacing:.2px}
.chip.tema{color:#0b0f16;border:none}
.msg{font-family:Georgia,"Times New Roman",serif;font-size:1.28em;line-height:1.5;color:#f5f1e6;
 padding:14px 16px;border-left:4px solid #d4af37;background:rgba(212,175,55,.06);border-radius:8px}
.ask{margin-top:14px;font-size:.9em;color:#67e8f9;font-weight:600}
hr#answer{border:none;height:1px;background:linear-gradient(90deg,transparent,#d4af37,transparent);margin:16px 0}
.ref{font-size:1.15em;font-weight:700;color:#facc15}
.cap,.trad2{font-size:.85em;color:#a5b4c3;margin-top:3px}
.box{margin-top:12px;padding:10px 12px;border-radius:10px;font-size:.95em}
.licao{background:rgba(34,211,238,.08);border:1px solid rgba(34,211,238,.35)}
.nerd{background:rgba(167,139,250,.08);border:1px solid rgba(167,139,250,.35)}
.selo{margin-top:12px;font-size:.75em;color:#8b98a8}
.selo b{color:#c9b37a}
.mito .msg{border-left-color:#ef4444;background:rgba(239,68,68,.07)}
.rev .q{font-size:1.25em;font-weight:700;color:#facc15}
.autor .msg{border-left-color:#e7c66a;background:linear-gradient(90deg,rgba(212,175,55,.14),rgba(212,175,55,.03));font-style:italic}
.autor .licao{background:rgba(212,175,55,.07);border-color:rgba(212,175,55,.45)}
.cred{margin-top:10px;padding-top:8px;border-top:1px dashed #3b3220;font-size:.7em;color:#9a8c66;letter-spacing:.2px}
.nightMode .card,.night_mode .card{background:#0b0f16}
@media (max-width:480px){.card{font-size:17px}.cx{margin:6px;padding:16px 14px}}
"""

FRENTE1 = """<div class="cx {{Classe}}">
<div class="top"><span class="chip">{{Baralho}}</span><span class="chip tema" style="background:{{Cor}}">{{Tema}}</span></div>
<div class="msg">“{{Mensagem}}”</div>
<div class="ask">{{Pergunta}}</div>
</div>"""

VERSO1 = """<div class="cx {{Classe}}">
<div class="top"><span class="chip">{{Baralho}}</span><span class="chip tema" style="background:{{Cor}}">{{Tema}}</span></div>
<div class="msg">“{{Mensagem}}”</div>
<hr id="answer">
<div class="ref">📍 {{Referencia}}</div>
{{#Capitulo}}<div class="cap">📚 {{Capitulo}}</div>{{/Capitulo}}
<div class="trad2">🏛️ {{Tradicao}}</div>
<div class="box licao">{{Licao}}</div>
{{#Curiosidade}}<div class="box nerd">🤓 <b>Curiosidade:</b> {{Curiosidade}}</div>{{/Curiosidade}}
<div class="selo">{{Selo}}</div>
<div class="cred">{{Creditos}}</div>
</div>"""

FRENTE2 = """{{#Reverso}}<div class="cx rev">
<div class="top"><span class="chip">{{Baralho}}</span><span class="chip tema" style="background:{{Cor}}">{{Tema}}</span></div>
<div class="q">📍 {{Referencia}}</div>
{{#Capitulo}}<div class="cap">📚 {{Capitulo}}</div>{{/Capitulo}}
<div class="ask">💬 Qual é a mensagem? Diga com suas palavras.</div>
</div>{{/Reverso}}"""

VERSO2 = """<div class="cx rev">
<div class="top"><span class="chip">{{Baralho}}</span><span class="chip tema" style="background:{{Cor}}">{{Tema}}</span></div>
<div class="q">📍 {{Referencia}}</div>
<hr id="answer">
<div class="msg">“{{Mensagem}}”</div>
<div class="box licao">{{Licao}}</div>
<div class="cred">{{Creditos}}</div>
</div>"""

CAMPOS = ["ID", "Mensagem", "Referencia", "Tradicao", "Baralho", "Tema", "Cor", "Capitulo", "Licao", "Curiosidade",
          "Selo", "Pergunta", "Classe", "Creditos", "Reverso"]

CONF = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "conferencia.json"))) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "conferencia.json")) else {}


def conf_txt(c):
    """Linha de conferência da referência (verify_escr.py, 16/11/2026)."""
    k = CONF.get(c["id"])
    if not k or c["selo"] == "autor":
        return ""
    if k["m"] == "fonte":
        return f" · 🔎 conferido no texto-fonte: {k['f']}"
    if k["m"] == "pendente":
        return " · 🔎 numeração a confirmar"
    return " · 🔎 revisado sem o texto-fonte à mão"


def montar(cards):
    modelo = genanki.Model(
        1786543211, "Escrituras & Axiomas 360X (v1.1)",
        fields=[{"name": f} for f in CAMPOS],
        templates=[{"name": "Mensagem → Fonte", "qfmt": FRENTE1, "afmt": VERSO1},
                   {"name": "Fonte → Mensagem (opcional)", "qfmt": FRENTE2, "afmt": VERSO2}],
        css=CSS, sort_field_index=0)
    pacote_decks = {}
    for i, c in enumerate(cards):
        nome_deck = f"{RAIZ}::{c['num']} {c['deck']}"
        if nome_deck not in pacote_decks:
            did = int(hashlib.md5(nome_deck.encode()).hexdigest()[:8], 16) + 1_800_000_000
            pacote_decks[nome_deck] = genanki.Deck(did, nome_deck)
        emo, tnome, cor = TEMAS[c["tema"]]
        mito = c["selo"] == "mito"
        autor = c["selo"] == "autor"
        nota = LINGUA_NOTA.get(c["lingua"], "Tradução livre")
        selo = {"canonico": f"✅ <b>Texto de fonte localizada</b> · {nota} · confira a redação no original",
                "tradicional": f"⚠️ <b>Atribuição tradicional</b> — fonte primária incerta · {nota}",
                "mito": "🕵️ <b>MITO DE ATRIBUIÇÃO</b> — a frase circula com o nome errado",
                "autor": f"⚜️ <b>Axioma autoral</b> · situação no catálogo: {c['meta']['sit'] if c['meta'] else ''} · {nota}"}[c["selo"]] + conf_txt(c)
        licao = (f"🔎 <b>Origem real:</b> {html.escape(c['licao'])}" if mito
                 else f"📖 <b>Comentário da edição:</b> {html.escape(c['licao'])}" if autor
                 else f"💡 <b>Lição:</b> {html.escape(c['licao'])}")
        pergunta = ("🕵️ A quem costumam atribuir — e quem disse de verdade?" if mito
                    else "⚜️ Que axioma do autor é este? (nome · eixo)" if autor
                    else "🔎 Qual é a fonte? (tradição · livro · capítulo/versículo)")
        credito = (f"✍️ Axioma de Aldenir Rocha de Oliveira Filho · Axiomas 360X nº {c['meta']['n']} · comentário da edição Códice 360X" if autor else CREDITO)
        tags = ["Escrituras360X", f"trad::{c['num']}_{slug(c['deck'])}", f"selo::{c['selo']}"]
        tags += [f"tema::{slug(TEMAS[t][1])}" for t in c["temas"]]
        if autor:
            tags += ["autor::Aldenir_Rocha", f"eixo::{slug(c['meta']['eixo'])}", f"situacao::{slug(c['meta']['sit'])}"]
        elif not mito:
            tags.append(f"obra::{slug(c['obra'])}")
            if c["cap"] is not None:
                tags.append(f"cap::{slug(c['obra'])}_{c['cap']:03d}")
        nota_anki = genanki.Note(
            model=modelo, guid=genanki.guid_for(c["id"]), tags=tags, due=i,
            fields=[c["id"], html.escape(c["msg"]), html.escape(c["ref"]), html.escape(c["trad"]),
                    html.escape(f"{c['num']} {c['deck']}"), f"{emo} {tnome}", cor, html.escape(c["capinfo"]),
                    licao, html.escape(c["nerd"]), selo, pergunta, "mito" if mito else ("autor" if autor else ""), credito, ""])
        pacote_decks[nome_deck].add_note(nota_anki)
    return list(pacote_decks.values())

def indice(cards, por_deck, decks):
    linhas = [f"# 📜 Escrituras & Axiomas 360X — índice ({VERSAO})", "",
              "**1145 flashcards** · 20 subbaralhos (19 tradições + ⚜️ Axiomas 360X do autor) · 15 temas · tags por obra e capítulo · arquivo `Escrituras_Axiomas_360X_1145_flashcards.apkg`", "", f"Créditos: {CREDITO}", "",
              "## 🗂️ Subbaralhos", "", "| # | Subbaralho | Cards |", "|---|---|---|"]
    for num, nome, *_ in decks:
        linhas.append(f"| {num} | {nome} | {por_deck[num]} |")
    linhas += ["", "## 🏷️ Temas (tag `tema::…`)", "", "| Tema | Cards | Busca no Anki |", "|---|---|---|"]
    ct = Counter(c["tema"] for c in cards)
    for k, (e, n, _) in TEMAS.items():
        linhas.append(f"| {e} {n} | {ct[k]} | `tag:tema::{slug(n)}` |")
    linhas += ["", "## 🛡️ Selos", "",
               f"- ✅ Texto de fonte localizada: {sum(c['selo']=='canonico' for c in cards)}",
               f"- ⚠️ Atribuição tradicional (fonte primária incerta): {sum(c['selo']=='tradicional' for c in cards)}",
               f"- 🕵️ Mito de atribuição: {sum(c['selo']=='mito' for c in cards)}",
               f"- ⚜️ Axioma autoral: {sum(c['selo']=='autor' for c in cards)}", "",
               "## 📚 Cards por subbaralho (referência · tema)", ""]
    for num, nome, *_ in decks:
        linhas.append(f"### {num} · {nome}")
        for c in [x for x in cards if x["num"] == num]:
            linhas.append(f"- {c['ref']} · {TEMAS[c['tema']][0]}")
        linhas.append("")
    return "\n".join(linhas)

def main():
    decks, cards, erros = carregar()
    por_deck, avisos = validar(decks, cards, erros)
    print(f"cards: {len(cards)} | subbaralhos: {len(por_deck)}")
    for k in sorted(por_deck):
        print(f"  {k}: {por_deck[k]}")
    print(f"erros: {len(erros)}"); [print("  ✗", e) for e in erros]
    print(f"avisos: {len(avisos)}"); [print("  •", a) for a in avisos]
    if erros:
        sys.exit(1)
    base = "Escrituras_Axiomas_360X_1145_flashcards"
    genanki.Package(montar(cards)).write_to_file(os.path.join(OUT, base + ".apkg"))
    with open(os.path.join(OUT, base + ".csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "subbaralho", "tradicao", "referencia", "capitulo", "tema", "mensagem", "licao_ou_origem_real", "curiosidade", "selo"])
        for c in cards:
            w.writerow([c["id"], f"{c['num']} {c['deck']}", c["trad"], c["ref"], c["capinfo"],
                        f"{TEMAS[c['tema']][0]} {TEMAS[c['tema']][1]}", c["msg"], c["licao"], c["nerd"], c["selo"]])
    with open(os.path.join(OUT, "INDICE_Escrituras_Axiomas_360X.md"), "w", encoding="utf-8") as f:
        f.write(indice(cards, por_deck, decks))
    print("ok →", OUT)

if __name__ == "__main__":
    main()
