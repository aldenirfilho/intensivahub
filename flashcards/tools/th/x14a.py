TXT = r"""
@A 🔥 SOFA: pontuação cardiovascular e respiratória?
| Pontos | Cardiovascular | Respiratório (P/F) |
| 1 | PAM < 70 | < 400 |
| 2 | Dopamina ≤ 5 ou dobutamina | < 300 |
| 3 | Dopamina > 5 ou **noradrenalina ≤ 0,1** | **< 200 com suporte ventilatório** |
| 4 | Dopamina > 15 ou **noradrenalina > 0,1** | **< 100 com suporte** |
^ Vincent 1996
@A 🔥 Calibração × discriminação de um escore prognóstico?
- **Discriminação**: separar quem morre de quem sobrevive → **área sob a curva ROC**
- **Calibração**: concordância entre mortalidade prevista e observada nas faixas de risco → **Hosmer-Lemeshow**, curva de calibração
= Um escore pode discriminar bem e estar descalibrado (superestimar mortes) em outra população ou época.
^ Epidemiologia clínica
@A 🔥 Densidade de incidência de infecção e taxa de utilização de dispositivo?
- Densidade = **(nº de infecções ÷ nº de dispositivos-dia) × 1.000**
- Taxa de utilização = **dispositivos-dia ÷ pacientes-dia**
= Usar dias de dispositivo no denominador corrige pela exposição.
^ ANVISA · CDC/NHSN
@A 🔥 Indicadores clássicos de desempenho da UTI?
- Mortalidade padronizada e uso padronizado de recursos
- **Readmissão em 48 h**
- Densidade de infecções associadas a dispositivos
- Taxa de ocupação e tempo de permanência
- Extubação não planejada, lesão por pressão, quedas, eventos adversos com medicação
^ ANVISA · AMIB
@B 🔥 UTI fechada e intensivista 24 horas: evidência?
- Modelo **fechado/alta intensidade** (intensivista conduz ou é consultado obrigatoriamente): menor mortalidade e permanência
- **Intensivista presencial à noite**: sem benefício adicional onde já há cobertura diurna de alta intensidade
^ Pronovost 2002 · Kerlin 2013
@B 🔥 Times de resposta rápida: braços e evidência?
- **Aferente**: detecção por critérios/escores de alerta precoce (NEWS2)
- **Eferente**: equipe que atende à beira do leito
- MERIT (ensaio em cluster): **sem redução** de PCR, morte ou admissão não planejada; estudos antes-depois sugerem benefício
^ MERIT Lancet 2005
@B 🔥 Checklist diário e metas multiprofissionais (CHECKLIST-ICU)?
= Ensaio em cluster em 118 UTIs brasileiras: **sem redução de mortalidade hospitalar**; melhora de processos (volume corrente baixo, menos sedação profunda, retirada de cateteres) e do clima de segurança.
^ Cavalcanti JAMA 2016
@B 🔥 Modelo do queijo suíço e cultura justa?
= Eventos adversos ocorrem quando **falhas latentes do sistema** se alinham a falhas ativas (Reason).
- **Cultura justa**: não punir o erro honesto; analisar o sistema; responsabilizar apenas conduta imprudente ou violação deliberada
- Classificação: **quase erro** (near miss), evento sem dano, evento adverso, **evento sentinela**
^ Reason 2000 · OMS
@B 🔥 Ferramentas de análise de risco: reativas × proativas?
- **Análise de causa raiz / Protocolo de Londres**: depois do evento (reativa)
- **FMEA** (análise de modos de falha e efeitos): antes do evento, prioriza por gravidade × ocorrência × detecção (proativa)
- **PDCA**: ciclo de melhoria contínua
^ Gestão da qualidade em saúde
@B 🔥 Passagem de plantão estruturada: I-PASS?
= **I**llness severity (gravidade) · **P**atient summary (resumo) · **A**ction list (pendências) · **S**ituation awareness (contingências) · **S**ynthesis by receiver (quem recebe repete).
- Reduziu erros médicos e eventos adversos evitáveis em estudo multicêntrico
^ Starmer NEJM 2014
@B 🔥 Precauções por aerossóis: quais doenças e quais medidas?
= **Tuberculose pulmonar/laríngea, sarampo, varicela/zóster disseminado**; e procedimentos geradores de aerossol em vírus respiratórios emergentes.
= Quarto privativo com **pressão negativa**, máscara **N95/PFF2** para a equipe, máscara cirúrgica no paciente em transporte.
^ CDC · ANVISA
@B 🔥 Visita familiar ampliada na UTI (ICU Visits)?
= Visita flexível de até 12 h × restrita (1,5 h): **não reduziu delirium**; **reduziu ansiedade e depressão dos familiares** e aumentou a satisfação, sem mais infecções nem burnout da equipe.
^ Rosa JAMA 2019
@B 🔥 Síndrome de burnout: três dimensões?
= **Exaustão emocional**, **despersonalização** (cinismo, distanciamento) e **baixa realização profissional**.
- Na UTI, associada a conflitos, decisões de fim de vida e sobrecarga; afeta a segurança do paciente
^ Maslach · Moss 2016
@C 🔥 Recusa de transfusão por adulto capaz: entendimento do STF (2024)?
= Testemunha de Jeová **maior e capaz** pode recusar transfusão, desde que a decisão seja **livre, informada, inequívoca e do próprio paciente**; o Estado deve oferecer alternativas disponíveis no SUS.
! Não vale para decisão dos pais por **menor de idade** em risco de vida.
^ STF · RE 979.742 e RE 1.212.272
@C 🔥 Não iniciar × retirar suporte: há diferença ética?
= **Não**: são moralmente equivalentes quando o tratamento não atende aos objetivos do cuidado. Retirar exige mais preparo e comunicação, mas não é "pior".
= Decisão compartilhada, registrada em prontuário, com cuidados de conforto mantidos.
^ ATS 2008 · AMIB
@C 🔥 Extubação paliativa: preparo?
- Reunião familiar e registro da decisão
- **Suspender o bloqueador neuromuscular e aguardar a reversão**
- Opioide e benzodiazepínico em dose para conforto **antes** da retirada; antissecretor
- Suspender dieta e fluidos em excesso; desligar alarmes; família presente se desejar
^ Truog 2008
@C 🔥 Comunicação com a família na UTI: mnemônicos VALUE e NURSE?
- **VALUE**: **V**alorizar o que dizem, **A**colher emoções, **L**isten (ouvir), **U**nderstand (conhecer o paciente como pessoa), **E**licit (provocar perguntas)
- **NURSE** (resposta à emoção): **N**omear, **U**nderstand, **R**espeitar, **S**uporte, **E**xplorar
= Conferência familiar estruturada reduz estresse pós-traumático dos familiares.
^ Lautrette NEJM 2007
@C 🔥 Morte encefálica: comunicação e doação?
- Informar o **óbito** com clareza; evitar "manter vivo por aparelhos"
- **Separar** a notícia da morte da entrevista sobre doação (feita por equipe treinada)
- No Brasil a doação depende de **autorização familiar** (cônjuge ou parente até o 2º grau)
- Recusa familiar: suspender o suporte (CFM 1.826/2007)
^ Lei 9.434/1997 · Decreto 9.175/2017
@D 🔥 Índice de fragilidade de um ensaio clínico?
= Número mínimo de pacientes que, mudando de "sem evento" para "evento", faria o resultado **perder a significância**.
- Muitos ensaios de terapia intensiva têm índice ≤ 5, menor que as perdas de seguimento
^ Walsh 2014 · Ridgeon 2016
@D 🔥 Análise bayesiana de ensaios "negativos": para que serve?
= Estima a **probabilidade de benefício** dado o resultado e o conhecimento prévio, em vez de um corte de p.
- Exemplo: EOLIA (p = 0,09) → probabilidade alta de alguma redução de mortalidade com ECMO
^ Goligher JAMA 2018
@D 🔥 Dias livres de ventilação como desfecho: cálculo e crítica?
= Dias vivo **e** sem ventilador até o dia 28; **morte = zero**.
! Mistura mortalidade e duração: efeitos opostos podem se anular; preferir análise hierárquica (win ratio) ou desfechos separados.
^ Yehya 2019
@D 🔥 Ensaios de plataforma adaptativos: como funcionam?
= Protocolo-mestre perene que testa **várias intervenções ao mesmo tempo**, com análises interinas, entrada e saída de braços e, às vezes, randomização adaptada à resposta.
- Exemplos: **REMAP-CAP** e **RECOVERY**
^ Angus 2019
@D 🔥 Ensaio em cluster com cruzamento: vantagens e riscos?
= Unidades inteiras alternam a intervenção por períodos (ex.: SMART, com fluidos por mês).
- Vantagem: logística simples e grandes amostras
- Riscos: **contaminação entre períodos**, falta de cegamento, necessidade de ajustar pela correlação intracluster
^ Semler 2018
"""
