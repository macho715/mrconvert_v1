좋아, 개념부터 뼈대까지 한 번에 잡자. **“고정밀 OCR·구조화 지침 v2.4 – LDG Ready”**를 온톨로지 관점으로 보면, 단순 파이프라인이 아니라 “문서→추출→정제→검증→감사”로 이어지는 **의미 그래프**다. 핵심은 각 단계가 **명시적 클래스와 관계**로 연결되고, KPI와 Fail-safe가 **제약(Constraint)** 으로 모델에 박혀 있다는 점.

---

# 1) 상위 온톨로지 스키마(개념 지도)

**핵심 클래스**

* `ldg:Document` (CI/PL/BL/Invoice 등), `ldg:Page`, `ldg:Image`
* `ldg:OCRBlock / OCRToken`(conf 포함), `ldg:Table`(Schema/Type/Footnote 메타)
* `ldg:RefinedText`(형식·단위 보정 결과), `ldg:EntityTag`(Shipper/Consignee/BL_No/…)
* `ldg:Payload`(= LDG_PAYLOAD), `ldg:Audit`(= LDG_AUDIT)
* `ldg:Metric`(MeanConf, TableAcc, NumericIntegrity, EntityMatch)
* `ldg:Validation`(Auto-Validation 5단계), `ldg:CrossLink`(CIPL↔BL↔PL)
* `ldg:RegTechFlag`(MOIAT/FANR/IMDG/Dual-Use), `ldg:HSCandidate`
* `ldg:CostGuardCheck`(표준요율 대비, FX 잠금)

**주요 관계**

* `ldg:hasPage`, `ldg:hasImage`, `ldg:hasOCR`, `ldg:hasTable`
* `ldg:refines`(Raw→Refined), `ldg:tagsEntity`(엔티티 자동 태깅)
* `ldg:buildsPayload`(정제 산출→LDG_PAYLOAD)
* `ldg:validatedBy`(5단계 자동 검증), `ldg:hasMetric`
* `ldg:hasAudit`, `ldg:hasHash`(image/text hash), `ldg:crossLinksTo`
* `ldg:triggersRegTech`, `ldg:proposesHS`
* `ldg:evaluatedByCostGuard`(FX lock, 초과율 판단)

> 위 클래스/관계는 문서의 단계·KPI·RegTech 훅·CostGuard 정책 서술을 **개념 객체**로 옮긴 것. (업로드→Pre-Prep→Vision OCR→Smart Table Parser 2.1→NLP Refine→Field Tagger→Payload Builder→Auto-Validation 5단계→LDG+ 출력→HITL 승인→Report Lock)

---

# 2) 프로세스 → 온톨로지 상태머신

```
ldg:Document
  ├─(ldg:hasImage)→ ldg:Image
  ├─(ldg:hasOCR)→ ldg:OCRBlock/Token(conf)
  ├─(ldg:hasTable)→ ldg:Table(type, unit/currency split, footnote)
  ├─(ldg:refines)→ ldg:RefinedText(??, (추정·Med) 명시)
  ├─(ldg:tagsEntity)→ ldg:EntityTag(Shipper/BL_No/Incoterms…)
  ├─(ldg:buildsPayload)→ ldg:Payload(LDG_Version, Trade, Logistics…)
  ├─(ldg:validatedBy)→ ldg:Validation(5단계, 적합도%)
  │    └─(ldg:hasMetric)→ ldg:Metric(MeanConf/TableAcc/NumericIntegrity/EntityMatch)
  ├─(ldg:hasAudit)→ ldg:Audit(SelfCheck/Totals/CrossDoc/Hash)
  ├─(ldg:crossLinksTo)→ ldg:CrossLink(CIPL↔BL↔PL)
  ├─(ldg:triggersRegTech)→ ldg:RegTechFlag(MOIAT/FANR/IMDG/DualUse)
  └─(ldg:evaluatedByCostGuard)→ ldg:CostGuardCheck(FX locked, exceed_pct, verdict)
```

* **KPI 게이트**(MeanConf≥…, TableAcc≥…, NumericIntegrity=100%, EntityMatch≥…, HashConsistency=PASS)는 `ldg:Validation`의 **필수 제약조건**으로 모델링 → 미달 시 `ldg:FailState(ZERO)`로 전이.
* **HallucinationBan/Deterministic** 규칙은 `ldg:RefinedText`와 `ldg:Payload`에 **표현 제약**으로 귀속(불명확=“??”, 추정=“(추정·Med)”, 합계 오차 ±0.00 고정).

---

# 3) 데이터 스키마 매핑 (LDG_PAYLOAD/AUDIT → 그래프)

**예시 매핑(개념)**

* `payload.DocType` → `ldg:Payload ldg:docType`
* `Parties.Shipper/Consignee` → `ldg:EntityTag ldg:partyRole`
* `Ids.BL_No/Invoice_No` → `ldg:Identifier ldg:idValue`
* `Logistics.(Packages,GW,NW,CBM)` → `ldg:CargoStat`
* `Trade.(Incoterms,Origin,Destination)` → `ldg:TradeTerm`
* `Currency, Total_Amount` → `ldg:MonetaryTerm`
* `HS_Candidates[]` → `ldg:HSCandidate(ldg:code, ldg:confidence)`
* `RegTechFlags` → `ldg:RegTechFlag` (MOIAT/FANR/IMDG/DualUse)
* `Metrics` → `ldg:Metric` (검증 노드에 연결)
* `Hashes.image/text` → `ldg:HashDigest`
* `CrossLinks.PL_No` → `ldg:CrossLink`(문서 간 참조)
* `LDG_AUDIT.SelfCheck/TotalsCheck/CrossDocCheck/HashConsistency/Warnings` → `ldg:Audit` 하위 속성

문서에 정의된 JSON 구조를 위와 같이 온톨로지로 승격하면, **문서·값·검증·감사**가 한 그래프 위에서 **질의/추적/잠금** 가능.

---

# 4) 제약(Constraints)과 Fail-safe의 온톨로지 표현

* **SHACL 제약**(개념 초안)

```turtle
# NumericIntegrity = 100% (라인합=수량×단가 ∧ 합계 일치 ∧ 통화/FX 일관)
ldg:NumericIntegrityShape a sh:NodeShape ;
  sh:targetClass ldg:Validation ;
  sh:property [
    sh:path ldg:numericIntegrity ;
    sh:datatype xsd:decimal ;
    sh:minInclusive 1.00 ; sh:maxInclusive 1.00
  ] .
```

* **ZERO Fail-safe**: 아래 중 하나라도 위반 시 `ldg:Validation ldg:state ldg:ZERO`
  (MeanConf/TableAcc/EntityMatch 기준 미달, NumericIntegrity≠100%, HashMismatch 등).

---

# 5) JSON-LD 컨텍스트(요약 예시)

```json
{
  "@context": {
    "ldg": "https://example.com/ldg#",
    "docType": "ldg:docType",
    "partyRole": "ldg:partyRole",
    "idValue": "ldg:idValue",
    "numericIntegrity": "ldg:numericIntegrity",
    "meanConf": "ldg:meanConf",
    "tableAcc": "ldg:tableAcc",
    "entityMatch": "ldg:entityMatch",
    "hashImage": "ldg:hashImage",
    "hashText": "ldg:hashText",
    "fxSource": "ldg:fxSource",
    "fxLocked": "ldg:fxLocked",
    "exceedPct": "ldg:exceedPct",
    "verdict": "ldg:verdict"
  }
}
```

이 컨텍스트를 쓰면 LDG_PAYLOAD/LDG_AUDIT JSON이 곧바로 **지식 그래프 문서화**된다(질의·감사·재현성 ↑).

---

# 6) 질의·감사 시나리오(예)

* **합계 무결성 점검**: `SELECT` 그래프 질의로 `(qty×unitPrice)=lineTotal` 전 행 검증 → `doc_total`과 일치 확인(±0.00). 미일치 시 해당 `ldg:Validation`을 `ldg:ZERO`로 전이.
* **Cross-Doc 일관성**: `PL→CI weights`, `CIPL→BL pkgs`를 `ldg:CrossLink`로 추적, `ldg:Audit.CrossDocCheck` PASS/FAIL 로그 축적.
* **RegTech 트리거**: HS 후보/키워드로 MOIAT/FANR/IMDG/Dual-Use 플래그 세팅, 최종 결론은 사람 승인(HITL)로 잠금.
* **Cost-Guard**: `std rate` vs `draft rate` 초과율 계산 + FX 잠금 정책(`fx_source`, `fx_locked`)을 그래프에 기록, 항목별 리스크와 `verdict` 집계.

---

# 7) 운영 원칙의 온톨로지 내재화(요점)

* **HallucinationBan**: 값 부재는 `null`, 불명확은 `"??"`, 추정은 `"(추정·Med)"`로 **상태값**을 분리—모델이 *모른다*는 사실을 표현.
* **Deterministic 수리 규칙**: 소수점·합계·환율·단위 고정 → 모든 계산은 **재현 가능 함수**(Audit에 로그).
* **KPI 게이트**: KPI는 단순 숫자가 아니라 **통과 조건**. 온톨로지에서 SHACL/규칙으로 강제.
* **HITL & Report Lock**: 승인 전 체크리스트와 해시/타임스탬프로 **불변 스냅샷**을 남김(Changelog 누적).

---

# 8) 바로 쓰는 최소 구현 순서(현장 적용용)

1. **네임스페이스/컨텍스트** 확정(`ldg:`), 문서키(`doc_hash`+파일 메타) 생성.
2. **스키마 실체화**: `ldg:Document/Validation/Audit/Metric/RegTech/CostGuard` 클래스와 속성 발행.
3. **파이프라인 이벤트→트리플**: 각 스텝 산출물(표, 태그, KPI)을 즉시 그래프에 `Append`.
4. **KPI/Fail-safe SHACL** 배치: 미달 즉시 `ldg:ZERO` 상태 전이 + 중단 로그.
5. **HITL 승인 시 Report Lock**: 해시/서명/타임스탬프 고정, 재생성 시 Changelog 추가.

---

원하는 만큼 깊게 들어갈 수 있는데, 여기까지면 뼈대는 잡혔다.
다음 스텝으로, 네가 쓰는 **RDF/JSON-LD 템플릿**이나 **SHACL 세트**를 바로 만들어줄 수도 있어. 어떤 문서타입(CI/PL/BL/Invoice)부터 묶을지만 콕 집어줘.
