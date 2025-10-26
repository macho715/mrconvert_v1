
나의 말:
/list
ChatGPT의 말:
여기 최신 /list 명령어 기준으로 정리된 전체 명령어·모드 세트입니다.
버전: Slash Commands & Modes List v2.1 (2025-10-22)

🧭 Core Logistics Commands
Command	Description	Typical Merge
`/logi-master [--fast	--deep	--AEDonly
`/switch_mode PRIME	ORACLE	ZERO
/visualize_data --type=heatmap <csv>	Heat-Stow, WH/Deck Pressure Heatmap
/wh-capacity oracle --horizon 12m	Warehouse Forecast 시뮬레이션	/switch_mode ORACLE
/redo step <stage>	스테이지별 재실행	/logi-master 연동
⚙️ Automation & Workflow
Command	Description
/automate_workflow	전체 프로세스 자동 실행 (RPA+LLM)
/save_template <name> / /use_template <name>	프롬프트 템플릿 저장·불러오기
/schedule_email	이메일 예약 발송
/analyze_text	텍스트 기반 패턴·의도 분석
/ontology-mapper	CSV/ERP → RDF/OWL 온톨로지 매핑
/revalidate	재검증 및 통합 유효성 체크
/search-mandate	규정·정책 검색 (MOIAT/FANR 등)
/generate-CNTR-map	컨테이너 경로/흐름 맵 생성
/logi-meta list	현재 등록된 모듈/옵션 리스트 출력
🧮 Advanced Analysis
Command	Description
/if-logic <cond> --on_fail=<action>	조건부 실행 제어
/compare_options --min=3	다중 옵션 비교 테이블
/check_KPI <metric> --threshold=<val>	KPI 기준 검증
`/ToT_mode [--deep	--tree]`
/self_consistency --n=3	다각도 검증 후 일치 답만 채택
/optimize_prompt --auto --freq=weekly	자동 프롬프트 튜닝
🧠 Meta / Evaluation
Command	Description
/prompt audit	프롬프트 품질·일관성 감사
/LIST	현재 전체 명령어·모드 세트 조회
/check_KPI PromptReuse --threshold=0.90	프롬프트 재활용률 모니터링
/switch_mode COST-GUARD + /logi-master invoice-audit	자동 청구감사 트리거
/switch_mode RHYTHM + /logi-master kpi-dash --KRsummary	KPI 대시보드 리포트
📡 Aegis Persona
Trigger	Description
“Aegis, online”	시스템 모드 전환: 분석 + 결단 중심
“Aegis, standby”	Aegis 로그 비활성화
Output	Aegis Answer, Aegis Log, One ruthless question
🧩 Fail-Safe & Templates
ZERO Mode: 데이터·법적 근거 불충분 시
→ “중단” 로그 테이블만 출력

DualBrain_Prompt_Frame_v1: 구조화 보고서 템플릿
(Role → Context → Task → Constraints → Evidence → Exec → Visual → Options → Roadmap → Review)

필요 시 /logi-meta list 로 모듈별 상세 옵션을,
또는 /switch_mode [MODE] + /logi-master [TASK] 로 병합 실행 테스트 가능합니다.

나의 말:
/logi meta list
ChatGPT의 말:
/logi-meta list — Registered Modules (v2.1 · 2025-10-22)
ExecSummary (KR+EN)
현재 등록된 워크플로/유틸 모듈과 옵션 플래그 요약.

기본 출력: 2-dec, ISO 날짜, NDA/PII 마스킹.

Incoterms/HS/3PL·WMS·DEM/DET·stowage 연계 가능(모듈별 표기).

Visual (Table)
Group	Module (Command)	Purpose	Key Flags/Args	Inputs	Outputs
Core	invoice-audit (/logi-master)	청구·단가 감사(COST-GUARD)	--fast --deep --AEDonly	Draft Inv, PDF SoR/ToR, cost_table	PASS/FAIL tbl, Δ%, recovery AED
Core	predict (/logi-master)	WH/운송 수요·ETA 예측	--h=12m --noheatmap	WMS/IO, voyage, weather	Forecast CSV/PNG, KPI
Core	kpi-dash (/logi-master)	KPI 리포트(OTIF, DEM/DET)	--KRsummary	Ops logs, WMS, voyage	Markdown rpt, spark figs
Core	weather-tie (/logi-master)	기상–운항 연계(berth/ETA)	--port=MW4 --vsl=JPTW71	Port metocean, ETA	Weather risk flags
Core	report (/logi-master)	상황·주간/월간 리포트	--scope=PORT/WH/FIN	Mixed ops data	PDF/MD summary
Compliance	cert-chk (/logi-master)	MOIAT/FANR 인증 트리거	--strict	HS Code, CI/PL	Cert matrix, gaps
Compliance	hs-risk (/logi-master)	HS 분류 리스크 스코어	--oracle	Desc, HS dict	Risk tiers, alt HS
Data/Ontology	/ontology-mapper	CSV/ERP→RDF/OWL 매핑	--schema hvdc_v3.8	CSV/ERP/WMS	TTL/JSON-LD, SHACL rpt
Data/Validation	/revalidate	재검증·정합성 체크	--all --fix	Prior outputs	Fix log, delta map
Geo/Flow	/generate-CNTR-map	CNTR 흐름 맵	--lane MIR→AGI	BL/DO/ATLP	Route PNG/GeoJSON
Viz	/visualize_data	Heat-Stow/WH heatmap	--type=heatmap <csv>	CSV (deck/yard)	PNG heatmap
Forecast	/wh-capacity oracle	WH 용량 예측	--horizon 12m	WMS IO	Util% curve
Meta	/prompt audit	프롬프트 감사	--scope=all	Chat logs	Scorecard
Meta	/optimize_prompt	자동 튜닝	--auto --freq=weekly	Logs	Tuned params
Reasoning	/ToT_mode	Tree-of-Thought	`--deep	--tree`	Any
QA	/self_consistency	다각도 검증	--n=3	Any	Agreed answer
Control	/if-logic	조건부 실행	--on_fail=<action>	Cond	Routed flow
KPI	/check_KPI	KPI 임계 검증	--threshold=<v>	Metrics	PASS/WARN
Email	/schedule_email	예약 발송	--at=YYYY-MM-DDThh:mm	Draft	Scheduled mail
Auto	/automate_workflow	RPA+LLM 파이프라인	--profile hvdc	Triggers	End-to-end run
Text	/analyze_text	텍스트 의도/패턴	--mode logistics	Free text	Tags/Entities
Options (Quick Combos)
비용감사: /switch_mode COST-GUARD + /logi-master invoice-audit --AEDonly --fast

KPI 리포트: /switch_mode RHYTHM + /logi-master kpi-dash --KRsummary

HS/인증: /switch_mode ORACLE + /logi-master hs-risk --oracle → 이어서 cert-chk --strict

Roadmap (P→Pi→B→O→S + KPI)
Prepare: cost_table/HS dict/WMS IO 최신화 (TableAcc ≥98.00%)

Pilot: invoice-audit 1주 시범(Δ% 검출율 ≥95.00%)

Build: Ontology+SHACL 통합, /ontology-mapper 표준화

Operate: Auto-run + /check_KPI DEMDET≤10.00% 게이트

Scale: Ports/WH 다사이트 확장, TG 알림 연동

Automation (Hooks)
Auto-Triggers: Invoice 파일 감지 → COST-GUARD / HS 언급 → ORACLE+cert-chk / Weather/ETA → weather-tie

Sheets/TG 연동: 결과 CSV→Sheets, 임계 초과 시 TG Ping.

QA (Gap/Recheck)
cost_table 버전·FX 고정 확인

HS dict 최신(YYYY-MM-DD) 확인

WMS 시계열 누락·중복 체크

ATLP/Maqta BL/DO 키 매칭 재검

CmdRec
/logi-master list (핵심 모듈 헬프)

/logi-meta list --verbose (세부 플래그/스키마)

/compare_options --min=3 (의사결정 테이블)

끝.

나의 말:
/logi-meta list --verbose
ChatGPT의 말:
/logi-meta list —verbose (v2.1 · 2025-10-22)
1) ExecSummary (KR+EN)
등록 모듈·플래그·입출력·사전조건·KPI·Fail-mode까지 풀스펙.

모든 수치 2-dec, ISO 날짜, NDA/PII 마스킹. Incoterms/HS/3PL·WMS/DEM-DET/stowage 연계 가능.

ZERO failsafe 규칙 포함(근거 부족 시 “중단” 로그만 출력).

2) Visual (Master Table)
Group	Module (cmd)	Purpose	Key Flags/Args	Inputs (min)	Output	KPI (target)	Preconditions	Fail-Modes
Core	/logi-master invoice-audit	청구·단가 감사(COST-GUARD)	--fast --deep --AEDonly --fx=locked	draft_inv, pdf_SoR/ToR, cost_table	Δ% tbl, PASS/FAIL	Overage≤2.00%	cost_table 최신, 통화식별	Missing rate, FX drift, line-map mismatch
Core	/logi-master predict	WH/운송 수요·ETA 예측	--h=12m --noheatmap	WMS IO, voyage log, weather	Forecast CSV/PNG	MAPE≤12.00%	Clean time index	Sparse IO, regime shift
Core	/logi-master kpi-dash	KPI 리포트	--KRsummary --period=YYYY-MM	Ops logs, WMS	Markdown rpt	TableAcc≥98.00%	Stable schemas	Mixed locales, null metrics
Core	/logi-master weather-tie	기상–운항 연계	--port=MW4 --vsl=JPTW71	metocean, ETA	Weather flags	OTIF≥95.00%	Valid ETA key	Port code mismatch
Core	/logi-master report	상황/주간/월간	--scope=PORT/WH/FIN	Mixed ops data	PDF/MD	SLA on-time≥95.00%	Scope defined	Section missing
Compliance	/logi-master cert-chk	MOIAT/FANR 트리거	--strict --hsdict=<ver>	HS code, CI/PL	Cert matrix	Auto-pass≥90.00%	HS map ok	Ambiguous HS
Compliance	/logi-master hs-risk	HS 분류 리스크	--oracle --topk=3	Desc, HS dict	Risk tiers	Dispute≤5.00%	Dict version pin	Polysemy
Data/Ont	/ontology-mapper	CSV/ERP→RDF/OWL	--schema=hvdc_v3.8 --emit=TTL,JSONLD	CSV/ERP/WMS	TTL, JSON-LD, SHACL rpt	Shape pass≥98.00%	Header map	Shape violations
Validation	/revalidate	재검증·수정	--all --fix --strict	Prior outputs	Fix log	Residual≤2.00%	Baseline present	Non-idempotent fix
Geo/Flow	/generate-CNTR-map	CNTR 흐름 맵	--lane MIR→AGI --fmt=PNG,GeoJSON	BL/DO/ATLP	Route viz	Lane match≥99.00%	Key join ok	Orphan legs
Viz	/visualize_data	Heatmap	--type=heatmap <csv>	deck/yard CSV	PNG heatmap	Render<5.00s	Clean grid	NaNs, units
Forecast	/wh-capacity oracle	WH 용량 예측	--horizon=12m --cap=<sqm>	WMS IO	Util% curve	Util≤85.00%	Cap defined	Cap drift
Meta	/prompt audit	프롬프트 감사	--scope=all --since=30d	chat logs	Scorecard	Reuse≥90.00%	Log access	Thin data
Meta	/optimize_prompt	자동 튜닝	--auto --freq=weekly	logs	Tuned params	QoQ↑≥5.00%	Baseline set	Over-fit
Reason	/ToT_mode	Tree-of-Thought	`--deep	--tree`	any	Plan	Solve-rate↑	None
QA	/self_consistency	다각도 검증	--n=3	any	Agreed ans	Var≤1.00σ	Deterministic chunking	Mode collapse
Control	/if-logic	조건부 실행	--on_fail=<action>	cond expr	Routed flow	Skip-error≤1.00%	Valid DSL	Branch loops
KPI	/check_KPI	KPI 게이트	--threshold=<v>	metrics	PASS/WARN	Gate fidelity≥99.00%	Metric defs	Unit mix
Email	/schedule_email	예약 발송	--at=YYYY-MM-DDThh:mm	draft	Scheduled	On-time≥99.00%	TZ pinned	TZ mismatch
Auto	/automate_workflow	RPA+LLM	--profile=hvdc --notify=TG	triggers	E2E run	Touch-time↓≥50.00%	Secrets set	Token limits
Text	/analyze_text	의도/패턴	--mode=logistics	free text	Tags/Entities	F1≥0.90	Model ver pinned	Domain drift
3) Options (Ready Combos · pros/cons/$/risk/time)
Invoice Guard Fast-lane

Cmd: /switch_mode COST-GUARD + /logi-master invoice-audit --AEDonly --fast

Pros: 빠른 Δ% 검출 | Cons: 세부 근거 축약 | $: 낮음 | Risk: 낮음 | Time: 5–15 min

HS→Cert Chain

Cmd: /switch_mode ORACLE + /logi-master hs-risk --oracle → cert-chk --strict

Pros: 인증 리스크 예방 | Cons: 초기 dict 정비 필요 | $: 중간 | Risk: 중간 | Time: 20–40 min

WH Capacity Gate

Cmd: /wh-capacity oracle --horizon 12m → /check_KPI WarehouseUtil --threshold=0.85

Pros: 과점유 사전 차단 | Cons: Cap 산정 의존 | $: 낮음 | Risk: 낮음 | Time: 15–30 min

4) Roadmap (Prepare→Pilot→Build→Operate→Scale + KPI)
Prepare: cost_table/HS dict/WMS IO 버전 고정, 헤더 매칭 룰 배포 (TableAcc ≥98.00%).

Pilot: 1~2 주, invoice-audit & hs-risk 소규모 검증 (Alert Precision ≥95.00%).

Build: /ontology-mapper + SHACL Shapes + SPARQL 게이트, TG 알림 연동.

Operate: /automate_workflow 일일 배치, /check_KPI DEMDET≤10.00% 자동 차단.

Scale: 멀티 포트/WH/벤더 확장, lineage/monitoring 대시보드.

5) Automation Notes (RPA+LLM+Sheets/TG)
Outputs→Sheets 자동 적재, Δ%≥2.01% 항목 TG 즉시 알림.

HS/MOIAT/FANR 키워드 감지 시 ORACLE 모드 오토 스위치.

FX는 기본 locked (AED/USD), override 시 로그 남김.

6) QA (Gap/Recheck Checklist)
cost_table, HS dict, WMS IO의 버전/스키마/단위 잠금 확인.

Incoterms 2020 표기 일관성(FOB/CIF/DAP 등) 및 통화 단위(USD/AED) 검증.

Header 매칭: 대소문자/공백/전각/약어 → 의미 기반 룰 통과 여부.

ATLP/Maqta 키( BL/DO ) 조인 충돌·중복 키 재확인.

7) CmdRec (Top-3)
/switch_mode COST-GUARD + /logi-master invoice-audit --AEDonly --fast

/switch_mode ORACLE + /logi-master hs-risk --oracle

/wh-capacity oracle --horizon 12m

8) ZERO Fail-safe (“중단” 템플릿)
단계	이유	위험	요청데이터	다음조치
중단	핵심 참조 누락(cost_table/HS dict/WMS IO)	잘못된 판단·금전 손실	최신 cost_table, HS dict 버전, 소스 파일 경로	데이터 수신 후 재실행
끝.

나의 말:
/suggest prompt
ChatGPT의 말:
좋아.
지금 네 상황 기준으로 바로 쓸 만한 프롬프트 세트를 몇 개 제안해볼게 — 자동화, 검증, 리포트 중심으로.

🧭 /suggest prompt — MACHO-GPT Context Pack (2025-10-22)
목적	프롬프트	설명
1️⃣ Invoice Audit Fast-Lane	/switch_mode COST-GUARD + /logi-master invoice-audit --AEDonly --fast	DSV·OFCO 인보이스 vs cost_table Δ% 자동감사. 결과: Δ%, Risk Tier, PASS/FAIL.
2️⃣ WH Forecast & KPI Gate	/switch_mode ORACLE + /wh-capacity oracle --horizon 12m	향후 12개월 창고 점유율 예측 + /check_KPI WarehouseUtil --threshold=0.85 KPI 자동검증.
3️⃣ HS Code Compliance Chain	/switch_mode ORACLE + /logi-master hs-risk --oracle → /logi-master cert-chk --strict	HS Code 리스크 → MOIAT/FANR 인증 자동 트리거.
4️⃣ Heat-Stow Visual Run	/logi-master --noheatmap predict → /visualize_data --type=heatmap hvdc_deck.csv	Deck 압력/적재 분포 heatmap 생성.
5️⃣ RHYTHM KPI Report	/switch_mode RHYTHM + /logi-master kpi-dash --KRsummary	주간/월간 KPI 자동요약 (OTIF·DEM/DET·WH Util%).
6️⃣ Ontology Validation Sweep	/ontology-mapper --schema hvdc_v3.8 → /revalidate --all --fix	RDF 변환 및 SHACL 정합성 검증·자동수정.
7️⃣ Weather-Tie ETA Guard	/switch_mode ORACLE + /logi-master weather-tie --port=MW4 --vsl=JPTW71	실시간 기상-ETA 상관 경고 및 항차 지연 예측.
📊 추천 실행 루프
Morning Ops: /switch_mode RHYTHM + /logi-master kpi-dash --KRsummary

Midday Audit: /switch_mode COST-GUARD + /logi-master invoice-audit --AEDonly --fast

Evening Forecast: /switch_mode ORACLE + /wh-capacity oracle --horizon 12m

⚙️ 확장 아이디어
/automate_workflow --profile hvdc : 세 가지 루프 자동화 (RPA+TG).

/check_KPI DEMDET --threshold=0.10 : 운항지연 즉시 경고.

/optimize_prompt --auto --freq=weekly : 사용 패턴 기반 성능 튜닝.

필요하면 내가 네 업무 흐름에 맞춰 “/suggest prompt --domain=finance” 식으로 세부 영역별 세트로 쪼개줄 수도 있다.
원해?

나의 말:
필요하면 내가 네 업무 흐름에 맞춰 “/suggest prompt --domain=finance” 식으로 세부 영역별 세트로 쪼개줄 수도 있다
ChatGPT의 말:
좋아, 그 확장 버전 이미 구상돼 있다.
--domain 옵션을 주면 워크플로에 맞는 전용 세트를 바로 뽑을 수 있어.

💼 /suggest prompt --domain=finance
(Invoice·CostGuard·Currency·Rate Audit 중심)

목적	프롬프트	설명
1️⃣ 단가 일치 감사	/switch_mode COST-GUARD + /logi-master invoice-audit --AEDonly --deep	Draft vs 계약단가 교차검증 (Δ%·FX·CostCenter 매핑).
2️⃣ 통화정합 검증	/logi-master invoice-audit --fx=locked --AEDonly → /check_KPI FXVariance --threshold=0.02	AED/USD 변동폭 2% 초과 시 FAIL.
3️⃣ Rate Table 업데이트 감시	/revalidate --scope=cost_table --fix	구버전 단가표 자동 갱신 + 수정 로그 생성.
4️⃣ 예산 초과 감지	/switch_mode COST-GUARD + /logi-master report --scope=FIN	지출 vs 예산 비교 → 오버런 항목 분류.
5️⃣ Recovery Tracker	/logi-master kpi-dash --scope=FIN	과지급 복구율·회수액 실시간 KPI.
⚙️ Finance Automation Loop
/automate_workflow --profile finance_guard
  ↳ /switch_mode COST-GUARD + /logi-master invoice-audit --AEDonly --fast
  ↳ /check_KPI FXVariance --threshold=0.02
  ↳ /logi-master report --scope=FIN
결과는 Sheets에 누적, Δ%≥2.01% 자동 TG 알림.

📊 KPI Gate (Finance)
Metric	Target	Trigger
Δ Rate %	≤ 2.00 %	PASS/FAIL
FX Variance %	≤ 2.00 %	WARN/CRITICAL
Recovery %	≥ 90.00 %	ALERT if < 80.00 %
원하면 --domain=marine, --domain=warehouse, --domain=ontology 같은 식으로도 쪼갤 수 있다.
어떤 도메인부터 확장해볼까?

나의 말:
Domain =ontology
ChatGPT의 말:
좋다.
/suggest prompt --domain=ontology 는 온톨로지 설계·매핑·검증·지식그래프 통합에 맞춘 세트다.
데이터 모델·정합성·RDF/SHACL까지 바로 이어서 실행 가능하다.

🧩 /suggest prompt --domain=ontology
(Palantir Ontology · RDF/OWL · HVDC Integration 중심)

목적	프롬프트	설명
1️⃣ 온톨로지 매핑 실행	/ontology-mapper --schema hvdc_v3.8 --emit=TTL,JSONLD	ERP·CSV를 RDF/OWL 구조로 변환, hvdc_code 기준 URI 생성.
2️⃣ SHACL 정합성 검증	/revalidate --all --fix --strict	TTL/JSON-LD 결과를 SHACL Shape로 검증 및 자동 수정.
3️⃣ 온톨로지 기반 문서 검증	/switch_mode LATTICE + /logi-master report --scope=DOCALIGN	CIPL·BL·PL 의미 기반 헤더 매핑·불일치 검출.
4️⃣ RDF 스파클 질의 점검	/analyze_text --mode=sparql	자연어 질의 → SPARQL 변환 테스트, RAG 응답 정확도 측정.
5️⃣ 온톨로지 버전 감사	/prompt audit --scope=ontology	hvdc_v3.x 버전 간 클래스·속성 diff 리포트 생성.
⚙️ Ontology Automation Loop
/automate_workflow --profile ontology_sync
  ↳ /ontology-mapper --schema hvdc_v3.8
  ↳ /revalidate --all --fix
  ↳ /switch_mode LATTICE + /logi-master report --scope=DOCALIGN
출력: ontology_rpt.ttl, validation_log.md, alignment_delta.csv
Sheets 업로드 + TG 알림 자동.

📊 KPI Gate (Ontology)
Metric	Target	Trigger
Shape Pass Rate	≥ 98.00 %	ALERT if <95.00 %
Header Match Acc	≥ 97.00 %	WARN if <90.00 %
Ontology Drift %	≤ 3.00 %	FAIL if >5.00 %
🔁 확장 콤보
/switch_mode ORACLE + /logi-master hs-risk --oracle → HS 분류 자동 온톨로지 주입

/switch_mode PRIME + /logi-master report --scope=SUPPLYTIME17 → 계약 클로즈 자동 RDF화

/ontology-mapper --schema hvdc_v3.8 + /generate-CNTR-map → 물류 흐름 그래프 연결

이 모드로 돌리면 LogiOntology 파이프라인 전체를 RDF/SHACL 기반으로 재정렬할 수 있다.
다음에 확장할 도메인 — marine, warehouse, 아니면 compliance 중 어디로 갈까?
