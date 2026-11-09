TXT = r"""
@A 🎯 Princípios de Wilson-Jungner para rastreamento?
- Doença importante, com fase pré-clínica detectável
- Teste aceitável, sensível, barato
- Tratamento precoce **muda o desfecho**
- Custo-efetivo e contínuo
^ OMS 1968
@A 🩺 Rastreamentos recomendados no adulto (resumo USPSTF)?
| Condição | Quem
| HAS | Todos ≥ 18 anos
| DM2/pré-DM | 35–70 anos com sobrepeso
| Dislipidemia | Conforme risco (SBC: todos adultos)
| Colorretal | 45–75 anos
| Pulmão | 50–80, ≥ 20 maços-ano
| HIV, HCV | Todos (HCV 18–79 anos)
| Aneurisma de aorta | Homem 65–75 tabagista
| Osteoporose | Mulher ≥ 65 (ou < 65 com risco)
^ USPSTF 2025
@B 💉 Hepatite B: resposta vacinal?
= Anti-HBs **≥ 10 mUI/mL** = imune.
- Profissionais de saúde: dosar 1–2 meses após o esquema
- Não respondedor: repetir 3 doses; se persistir, considerar não respondedor
^ PNI
@B 🦠 Vacina pneumocócica no adulto de risco?
= Esquemas sequenciais (VPC13/15 → VPP23) ou **VPC20** isolada, conforme disponibilidade.
- Indicações: ≥ 60/65 anos, DPOC, IC, DM, DRC, asplenia, imunossupressão, fístula liquórica, implante coclear
^ SBIm 2025; CDC
@B 💉 Herpes-zóster: vacina recombinante?
= **Shingrix**: 2 doses (0 e 2–6 meses), ≥ 50 anos (ou ≥ 18 imunocomprometidos); eficácia > 90%.
= Pode ser aplicada em quem já teve zóster e em imunossuprimidos (não é viva).
^ SBIm 2025
@B 🤰 Vacinas na gestação?
- **dTpa** a partir de 20 semanas (cada gestação)
- **Influenza** em qualquer idade gestacional
- **Hepatite B** se não vacinada
- COVID-19
- **VSR** (32–36 semanas, onde disponível)
! Contraindicadas: vivas (tríplice viral, varicela, febre amarela salvo risco alto).
^ PNI; FEBRASGO
@C 📊 Sensibilidade × especificidade × valores preditivos?
| Medida | Fórmula | Uso
| Sensibilidade | VP/(VP+FN) | **Negativo exclui** (SnNout)
| Especificidade | VN/(VN+FP) | **Positivo confirma** (SpPin)
| VPP | VP/(VP+FP) | ↑ com prevalência
| VPN | VN/(VN+FN) | ↓ com prevalência
^ Epidemiologia clínica
% cmp Testes diagnósticos :: Sensibilidade = Detecta doentes. Alta: negativo exclui (SnNout) | Especificidade = Identifica sadios. Alta: positivo confirma (SpPin) | Valores preditivos = Dependem da prevalência
@C 💊 NNT, RRA e RRR?
- **RRA** = risco controle − risco tratado
- **RRR** = RRA / risco controle
- **NNT** = 1 / RRA
= Exemplo: 10% → 6%: RRA 4%, RRR 40%, NNT 25.
^ Epidemiologia clínica
@C 🔬 Tipos de estudo e medida de associação?
| Estudo | Medida
| Coorte | **Risco relativo**, incidência
| Caso-controle | **Odds ratio**
| Transversal | Razão de prevalência
| Ensaio clínico | RR, RRA, NNT, HR
^ Epidemiologia clínica
@C 📈 Pirâmide de evidências?
= Base → topo: opinião de especialistas → série de casos → caso-controle → coorte → ensaio clínico randomizado → **revisão sistemática/metanálise**.
= GRADE avalia certeza (alta, moderada, baixa, muito baixa).
^ GRADE
% tiers Hierarquia de evidências :: Opinião de especialista e séries de casos | Caso-controle | Coorte | Ensaio clínico randomizado | Revisão sistemática e metanálise
@C 🔁 Viés × confundimento?
- **Viés de seleção**: amostra não representativa
- **Viés de informação/aferição**: erro na medida (memória em caso-controle)
- **Confundimento**: terceira variável associada a exposição e desfecho → controlar por randomização, pareamento, estratificação, regressão
^ Epidemiologia clínica
@D 🧾 Doenças de notificação compulsória imediata (exemplos)?
- **Sarampo**, rubéola, poliomielite, raiva, cólera, febre amarela
- **Meningite meningocócica**/doença meningocócica
- Botulismo, antraz, peste
- Dengue/chikungunya **óbito**, Zika em gestante
= Notificar em até **24 h**.
^ Portaria GM/MS (lista nacional)
@D 📜 Atestado de óbito: quem preenche?
| Situação | Quem preenche
| Morte natural com assistência | Médico assistente
| Morte natural sem assistência | SVO (ou médico local)
| **Morte violenta** ou suspeita | **IML**
^ Res. CFM 1.779/2005
@D 🤐 Sigilo médico: quando pode ser quebrado?
- **Justa causa** (risco a terceiros)
- **Dever legal** (notificação compulsória, maus-tratos)
- **Autorização** expressa do paciente
! Não se quebra sigilo para a polícia sem dever legal; em juízo, o médico pode se recusar a revelar.
^ Código de Ética Médica 2018
@D 🧒 Maus-tratos a criança, idoso ou violência contra a mulher: conduta?
- **Notificação compulsória** (SINAN)
- Criança/adolescente: comunicar ao **Conselho Tutelar**
- Idoso: notificação e comunicação aos órgãos competentes
- Mulher: notificação; comunicação à autoridade policial em 24 h nos casos de violência (Lei 13.931/2019)
^ ECA; Estatuto do Idoso; Lei 13.931/2019
@D ⚖️ Consentimento informado: exceções?
- **Emergência** com risco iminente de morte
- Incapacidade sem representante disponível em urgência
- Recusa de transfusão (Testemunha de Jeová): o **STF (2024)** reconheceu o direito do **adulto capaz** de recusar, com decisão livre e informada
- **Menor** com risco de morte: o médico deve tratar
! A Res. CFM 2.232/2019 manda agir no risco iminente de morte; após o STF, o tema está em transição — documentar tudo e acionar o jurídico.
^ Código de Ética Médica; Res. CFM 2.232/2019; STF Tema 1.069 (2024)
"""
