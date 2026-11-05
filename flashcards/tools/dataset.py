from cards_a import SEPSE, VM, HEMO, ACIDO, ELETRO
from cards_b import RENAL, NEURO, SED, CARDIO, INFEC
from cards_c import HEMATO, ENDO, GASTRO, TRAUMA, ETICA
from new_a import SEPSE2, VM2, HEMO2, ACIDO2, ELETRO2
from new_b import RENAL2, NEURO2, SED2, CARDIO2, INFEC2
from new_c import HEMATO2, ENDO2, GASTRO2, TRAUMA2, ETICA2

THEMES = [
 ("01","🦠","Sepse e Choque Séptico","sepse",SEPSE,SEPSE2,"AAABBBBBCDBCCDDDDDCB",
  {"A":"Definições e triagem","B":"Ressuscitação hemodinâmica","C":"Antimicrobianos e controle de foco","D":"Terapias adjuvantes e suporte"}),
 ("02","🫁","Ventilação Mecânica e SDRA","vm-sdra",VM,VM2,"AABBBFFCCCFBDDDEEEFC",
  {"A":"Definição de SDRA","B":"Ventilação protetora e modos","C":"Resgate da hipoxemia","D":"Desmame e extubação","E":"VNI, CNAF e via aérea","F":"Mecânica, monitorização e complicações"}),
 ("03","❤️","Hemodinâmica e Choque","hemodinamica",HEMO,HEMO2,"AAAABBBCDDDCEEECABBE",
  {"A":"Fisiologia e monitorização","B":"Fluidorresponsividade","C":"Drogas vasoativas","D":"Choque cardiogênico e suporte mecânico","E":"Choques obstrutivo, distributivo e especiais"}),
 ("04","⚗️","Distúrbios Ácido-Base","acido-base",ACIDO,ACIDO2,"AAAABBBBCCDBBBFEFFEE",
  {"A":"Abordagem e compensação","B":"Acidose de AG elevado e intoxicações","C":"Acidose de AG normal e ATR","D":"Alcalose metabólica","E":"Distúrbios respiratórios e mistos","F":"Stewart e lactato"}),
 ("05","🧂","Eletrólitos","eletrolitos",ELETRO,ELETRO2,"AAAAAAAEBBBBCCCDDDAA",
  {"A":"Sódio","B":"Potássio","C":"Cálcio","D":"Magnésio e fósforo","E":"Água, osmolalidade e poliúria"}),
 ("06","🫘","Rim, LRA e TRS","renal",RENAL,RENAL2,"AAACCCCCBDBBABBCCADD",
  {"A":"Definição e diagnóstico da LRA","B":"Causas e síndromes renais","C":"Terapia renal substitutiva","D":"Prevenção e manejo hídrico"}),
 ("07","🧠","Neurointensivismo","neuro",NEURO,NEURO2,"ABAAADDDCCCCEEGGFFBF",
  {"A":"Coma, PIC e HIC","B":"TCE","C":"AVC isquêmico e hemorrágico","D":"Hemorragia subaracnóidea","E":"Estado de mal epiléptico","F":"Neuromuscular e encefalopatias","G":"Morte encefálica"}),
 ("08","😴","Sedação, Analgesia e Delirium","sedacao",SED,SED2,"AAAABBBBCCCBDDEEEDDB",
  {"A":"Escalas e monitorização","B":"Sedativos e analgésicos","C":"Delirium e bundle ABCDEF","D":"Via aérea e bloqueio neuromuscular","E":"Síndromes tóxicas e abstinência"}),
 ("09","⚡","Cardiointensivismo e PCR","cardio-pcr",CARDIO,CARDIO2,"AAAAAABBCCCCCDDEEEDE",
  {"A":"PCR e ressuscitação","B":"Cuidados pós-PCR","C":"Arritmias","D":"Síndrome coronariana aguda","E":"IC aguda e emergências cardiovasculares"}),
 ("10","🧫","Infecção e Antimicrobianos","infeccao",INFEC,INFEC2,"AAAAEDCCBBBBADDEFFCC",
  {"A":"Infecções associadas à assistência","B":"Resistência bacteriana","C":"PK/PD e uso de antimicrobianos","D":"Infecções comunitárias graves","E":"Fungos e imunossuprimidos","F":"Doenças tropicais e endêmicas"}),
 ("11","🩸","Hematologia, Coagulação e Transfusão","hemato",HEMATO,HEMATO2,"AAAABBBBCCCDDDABCADE",
  {"A":"Coagulopatias e plaquetopenias","B":"Transfusão","C":"Anticoagulação e reversão","D":"Onco-hematologia de urgência","E":"Obstetrícia crítica"}),
 ("12","🍬","Endocrinologia no Crítico","endocrino",ENDO,ENDO2,"AAAAAAACCDDDBBDADDCB",
  {"A":"CAD e EHH","B":"Controle glicêmico","C":"Tireoide","D":"Adrenal, hipófise e corticoides","E":"Outras emergências endócrinas"}),
 ("13","🫃","Gastro, Fígado e Nutrição","gastro-nutricao",GASTRO,GASTRO2,"AAAABBBBCCCCCCDDDEEC",
  {"A":"Hemorragia digestiva","B":"Pancreatite","C":"Fígado","D":"Nutrição","E":"Abdome agudo e complicações abdominais"}),
 ("14","🚑","Trauma, Toxicologia e Ambiental","trauma-tox",TRAUMA,TRAUMA2,"AAAABBBCCCCCCCCDDDDA",
  {"A":"Trauma e choque hemorrágico","B":"Queimados e inalação","C":"Toxicologia","D":"Ambiental e animais peçonhentos"}),
 ("15","⚖️","Ética, Escores, Qualidade e POCUS","etica-escores-pocus",ETICA,ETICA2,"AAABBBCCCCDDDDCEEEAD",
  {"A":"Escores e qualidade","B":"Bioestatística e evidência","C":"POCUS e procedimentos","D":"Ética, legislação e terminalidade","E":"Pós-UTI e reabilitação"}),
]

def all_themes():
    out = []
    for num, emo, nome, slug, old, new, codes, subs in THEMES:
        assert len(old) == 20 and len(codes) == 20 and len(new) == 20, (num, len(old), len(new), len(codes))
        cards = []
        for k, c in enumerate(old):
            cards.append(dict(c, t=codes[k], orig="v1"))
        for c in new:
            assert c["t"] in subs, (num, c["t"])
            cards.append(dict(c, orig="v2"))
        order = list(subs.keys())
        cards.sort(key=lambda c: order.index(c["t"]))  # stable: groups by subtema
        for c in cards: c["sub"] = subs[c["t"]]
        out.append(dict(num=num, emo=emo, nome=nome, slug=slug, subs=subs, cards=cards))
    return out
