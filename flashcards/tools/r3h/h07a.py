TXT = r"""
@A 🔥 Carbapenemases: qual droga para cada uma?
| Enzima | Classe | Opção |
| **KPC** | A | Ceftazidima-avibactam, meropenem-vaborbactam, imipenem-relebactam |
| **OXA-48** | D | Ceftazidima-avibactam |
| **NDM/VIM/IMP** (metalo) | B | **Ceftazidima-avibactam + aztreonam** ou cefiderocol |
^ IDSA AMR 2024
% cmp Carbapenemases :: KPC = Ceftazidima-avibactam · meropenem-vaborbactam | OXA-48 = Ceftazidima-avibactam | Metalo (NDM) = CAZ-AVI + aztreonam · cefiderocol
@A 🔥 Pseudomonas DTR (difícil de tratar): opções?
= **Ceftolozana-tazobactam**, ceftazidima-avibactam, imipenem-relebactam, cefiderocol.
^ IDSA AMR 2024
@A 🔥 Acinetobacter resistente a carbapenêmico?
= **Sulbactam-durlobactam** + carbapenêmico (preferido) ou sulbactam em alta dose em combinação.
! Polimixina: nefrotoxicidade e eficácia inferior.
^ IDSA AMR 2024
@A 🔥 Stenotrophomonas maltophilia?
= Intrinsecamente resistente a carbapenêmico → **SMX-TMP**, minociclina, levofloxacino ou cefiderocol; **CAZ-AVI + aztreonam** em grave.
^ IDSA AMR 2024
@A 🔥 Bactérias com AmpC induzível (HECK-Yes): implicação?
= **H**afnia, **E**nterobacter, **C**itrobacter freundii, **K**lebsiella aerogenes, **Y**ersinia → evitar ceftriaxona em infecção grave mesmo se "sensível"; preferir **cefepime**.
^ IDSA AMR 2024
@A 🔥 Linezolida: efeitos adversos importantes?
- **Mielossupressão** (> 14 dias), neuropatia periférica e óptica
- **Síndrome serotoninérgica** com ISRS
- Acidose lática, hipoglicemia
^ Sanford
@A 🔥 Fluoroquinolonas: alertas?
- **Tendinopatia/ruptura** (idoso, corticoide, transplante)
- **Aneurisma/dissecção de aorta**, neuropatia, disglicemia, QT longo
- Miastenia: piora
^ FDA 2018
@B 🔥 PAC grave: quando cobrir MRSA e Pseudomonas?
= Só com **colonização/isolamento prévio** pelo germe ou internação + antibiótico IV nos últimos 90 dias **e fatores locais** — coletar culturas/PCR nasal MRSA e descalonar.
= PCR nasal MRSA negativa: alto VPN → suspender vancomicina/linezolida.
^ ATS/IDSA 2019
@B 🔥 Corticoide na PAC grave?
= **Hidrocortisona 200 mg/dia** em PAC grave internada em UTI ↓ mortalidade (CAPE COD); excluir influenza e aspergilose.
^ CAPE COD 2023 · ATS 2024
@B 🔥 Aspergilose associada à influenza/COVID: quando suspeitar?
= Paciente grave em VM com piora sem explicação → **galactomanana no lavado** (> 1,0) e cultura; voriconazol/isavuconazol.
^ ECMM/ISHAM
@B 🔥 Pneumocistose em não-HIV: perfil e pistas?
- Corticoide ≥ 20 mg/dia por ≥ 4 semanas, rituximabe, transplante, QT
- Evolução **rápida**, hipoxemia grave, **LDH alta**, β-D-glucana positiva
= Profilaxia com SMX-TMP nesse perfil.
^ ECIL 2016
@C 🔥 HIV: carga viral detectável após supressão — "blip"?
= Elevação isolada **< 200 cópias** com retorno a indetectável — não indica falha; **falha virológica: > 200 confirmada**.
^ DHHS 2024
@C 🔥 Cabotegravir injetável: usos?
- **PrEP** a cada 2 meses (superior ao TDF/FTC oral)
- Tratamento (cabotegravir + rilpivirina) a cada 1–2 meses em suprimidos
= **Lenacapavir** semestral: PrEP altamente eficaz (PURPOSE).
^ HPTN 083/084 · PURPOSE 2024
@C 🔥 Hepatite B + HIV: cuidado com a TARV?
= Esquema **deve conter tenofovir** (TDF/TAF) + lamivudina/entricitabina; suspender pode causar **flare** grave de HBV.
^ DHHS 2024
@D 🔥 TB: esquema de 4 meses (rifapentina-moxifloxacino)?
= **2HPZM/2HPM** (rifapentina + isoniazida + pirazinamida + moxifloxacino) em ≥ 12 anos com TB pulmonar sensível (Study 31).
^ CDC/OMS 2022
@D 🔥 TB multirresistente: esquema curto atual?
= **BPaLM** (bedaquilina + pretomanida + linezolida + moxifloxacino) por **6 meses**.
! Monitorar QT, neuropatia e mielossupressão.
^ OMS 2022 · TB-PRACTECAL"""
