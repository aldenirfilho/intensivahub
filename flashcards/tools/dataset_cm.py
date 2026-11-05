from cm_a import CARDIO, PNEUMO, NEFRO, ENDO, GASTRO
from cm_b import HEMATO, INFECTO, REUMATO, NEURO, ONCO
from cm_c import GERIATRIA, PSIQ, PREV, DERMATO, FARMACO
from cm_cardio_v3 import CARDIO3
CARDIO = CARDIO + [dict(c, orig="v3") for c in CARDIO3]

CM_THEMES = [
 ("01","🫀","Cardiologia","cardio",CARDIO,{"A":"Hipertensão arterial","B":"Insuficiência cardíaca crônica","C":"Fibrilação atrial e anticoagulação","D":"Valvopatias","E":"Coronariopatia crônica e lipídios","F":"Pericárdio e cardiomiopatias","G":"ECG e síncope"}),
 ("02","🫁","Pneumologia","pneumo",PNEUMO,{"A":"Asma","B":"DPOC","C":"Derrame pleural e nódulo","D":"Intersticiais, sono e circulação pulmonar"}),
 ("03","🫘","Nefrologia","nefro",NEFRO,{"A":"Doença renal crônica","B":"Glomerulopatias","C":"Litíase e infecção urinária","D":"Outras nefropatias"}),
 ("04","🍬","Endocrinologia","endo",ENDO,{"A":"Diabetes tipo 2","B":"Tireoide","C":"Adrenal e hipófise","D":"Osteometabólico"}),
 ("05","🫃","Gastroenterologia e Hepatologia","gastro",GASTRO,{"A":"Esôfago e estômago","B":"Intestino","C":"Hepatites","D":"Cirrose e hepatopatias crônicas"}),
 ("06","🩸","Hematologia","hemato",HEMATO,{"A":"Anemias","B":"Neoplasias hematológicas","C":"Hemostasia e trombose"}),
 ("07","🦠","Infectologia","infecto",INFECTO,{"A":"HIV/aids","B":"Tuberculose","C":"IST e sífilis","D":"Doenças endêmicas","E":"Vacinas e profilaxias"}),
 ("08","🦴","Reumatologia","reumato",REUMATO,{"A":"Artrite reumatoide","B":"LES e colagenoses","C":"Gota e cristais","D":"Espondiloartrites, vasculites e artrite séptica"}),
 ("09","🧠","Neurologia","neuro",NEURO,{"A":"Cefaleias","B":"Epilepsia","C":"Doenças neurodegenerativas e desmielinizantes","D":"Vascular, nervos e síncope"}),
 ("10","🎗️","Oncologia Clínica","onco",ONCO,{"A":"Rastreamento e genética","B":"Marcadores e síndromes paraneoplásicas","C":"Urgências e suporte oncológico"}),
 ("11","👴","Geriatria e Cuidados Paliativos","geriatria",GERIATRIA,{"A":"Avaliação geriátrica e síndromes","B":"Polifarmácia","C":"Cuidados paliativos"}),
 ("12","🧘","Psiquiatria na Clínica","psiq",PSIQ,{"A":"Depressão e ansiedade","B":"Psicofármacos","C":"Álcool e outras drogas"}),
 ("13","🩺","Medicina Preventiva","preventiva",PREV,{"A":"Rastreamentos","B":"Obesidade","C":"Estilo de vida e tabagismo"}),
 ("14","🧴","Dermatologia e Alergia","dermato",DERMATO,{"A":"Farmacodermias","B":"Urticária, anafilaxia e alergia a drogas","C":"Dermatoses e infecções de pele"}),
 ("15","💊","Farmacologia, Semiologia e Laboratório","farmaco",FARMACO,{"A":"Interações medicamentosas","B":"Semiologia","C":"Exames laboratoriais"}),
]

def cm_themes():
    out = []
    for num, emo, nome, slug, cards, subs in CM_THEMES:
        assert len(cards) >= 20, (num, len(cards))
        order = list(subs)
        cs = []
        for c in cards:
            assert c["t"] in subs, (num, c["t"])
            cs.append(dict(c, orig=c.get("orig", "cm1"), sub=subs[c["t"]]))
        cs.sort(key=lambda c: order.index(c["t"]))
        out.append(dict(num=num, emo=emo, nome=nome, slug="cm-" + slug, subs=subs, cards=cs))
    return out

# imagens novas para cards do TEMI (trecho da frente → imagem)
TEMI_IMG = {
 "Parâmetros <b>PK/PD</b>": "img_pk_pd.png",
 "<b>N-acetilcisteína</b> na intoxicação": "img_rumack.png",
 "Tratamento da <b>hipercalemia</b> em 3 etapas": "img_hiperk.png",
 "o que o <b>Na urinário</b> diz": "img_hipona.png",
 "Classes de <b>choque hemorrágico</b>": "img_choque_hemorragico.png",
 "<b>Vasoespasmo</b> pós-HSA": "img_hsa_timeline.png",
 "PEEP alta × baixa": "img_pv_pulmao.png",
 "<b>Curva ROC</b>": "img_roc.png",
 "Sistema <b>GRADE</b>": "img_piramide.png",
 "Manejo inicial da <b>CAD</b>": "img_cad.png",
}
