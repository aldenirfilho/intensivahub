TXT = r"""
@A 🔥 Proteína em dose alta no crítico (EFFORT Protein)?
= **≥ 2,2 × ≤ 1,2 g/kg/dia**: sem benefício em tempo até a alta com vida nem em mortalidade.
! Pior desfecho com dose alta em **lesão renal aguda** e disfunção orgânica grave (SOFA alto).
^ Heyland Lancet 2023
@A 🔥 Nutrição precoce no choque: enteral × parenteral (NUTRIREA-2)?
= Ventilados com vasopressor: mortalidade igual (37% × 35%), mas com enteral houve **mais isquemia intestinal, pseudo-obstrução, vômito e diarreia**.
^ Reignier Lancet 2018
@A 🔥 Restrição calórico-proteica na fase aguda (NUTRIREA-3)?
= **6 kcal/kg + 0,2–0,4 g/kg de proteína** × 25 kcal/kg + 1,0–1,3 g/kg na primeira semana, em ventilados com vasopressor.
- Mortalidade em 90 dias igual (41,3% × 42,8%)
- **Alta mais rápida** e **menos** vômito, diarreia, isquemia intestinal e disfunção hepática
^ Reignier Lancet Respir Med 2023
% cmp Nutrição na fase aguda do choque :: NUTRIREA-2 = Enteral precoce plena: mais isquemia intestinal | NUTRIREA-3 = Dose baixa na 1ª semana: recuperação mais rápida | EFFORT = Proteína alta: sem benefício · pior na lesão renal
@A 🔥 Parenteral suplementar precoce × tardia (EPaNIC)?
= Iniciar a parenteral no **dia 8** (em vez de 48 h) → **menos infecções**, menos tempo de ventilação e de UTI, alta mais precoce.
^ Casaer NEJM 2011
@A 🔥 Enteral × parenteral como via inicial (CALORIES)?
= Mortalidade em 30 dias **igual**; com a parenteral houve menos hipoglicemia e vômito, sem mais infecções.
= A via importa menos do que evitar a **hiperalimentação**.
^ Harvey NEJM 2014
@A 🔥 Dieta trófica × plena na SDRA (EDEN) e hipocalórica (PermiT)?
- **EDEN**: trófica por 6 dias = plena em dias livres de ventilação e mortalidade; menos intolerância
- **PermiT**: 40–60% das calorias com proteína plena = dieta padrão
^ EDEN 2012 · PermiT 2015
@A 🔥 Densidade calórica maior (TARGET)?
= Fórmula **1,5 × 1,0 kcal/mL** no mesmo volume: mais calorias entregues, **mortalidade em 90 dias igual**; mais regurgitação e hiperglicemia.
^ TARGET NEJM 2018
@A 🔥 Calorimetria indireta: o que mede e como calcula?
= Mede **consumo de O₂ e produção de CO₂**; equação de Weir: gasto = **(3,94 × VO₂ + 1,11 × VCO₂) × 1,44**.
- Quociente respiratório: 0,7 (gordura), 0,8 (proteína), 1,0 (carboidrato); **> 1,0** = hiperalimentação/lipogênese
- Imprecisa com FiO₂ > 0,6, fuga aérea e terapia renal contínua
^ ESPEN 2019
@A 🔥 Calorias "escondidas" na UTI?
- **Propofol**: 1,1 kcal/mL
- **Citrato** da terapia renal contínua: ~3 kcal/g
- **Glicose** dos diluentes e do dialisato
= Somar para não hiperalimentar (hipercapnia, esteatose, hiperglicemia).
^ ESPEN 2019
@A 🔥 Nutrição parenteral: limites dos macronutrientes?
- Glicose **≤ 5 mg/kg/min**
- Lipídio **≤ 1,5 g/kg/dia** (incluindo o propofol); reduzir se triglicerídeos > 400 mg/dL
- Aminoácidos 1,3–2,0 g/kg/dia conforme a fase
^ ESPEN 2019
@A 🔥 Dieta enteral e vasopressor: pode?
= Sim, com choque **controlado** (dose estável ou em queda, lactato caindo): começar baixo e observar distensão, resíduo e lactato.
! Não iniciar em choque não controlado, hipoxemia/acidose ameaçadoras, isquemia intestinal ou sangramento digestivo ativo.
^ ESPEN 2019
@A 🔥 Vitamina D em dose alta no crítico (VITdAL-ICU, VIOLET)?
= **Sem benefício** em mortalidade ou tempo de internação (VITdAL sugeriu benefício só na deficiência grave; VIOLET foi neutro).
^ Amrein 2014 · VIOLET 2019
"""
