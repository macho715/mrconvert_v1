# [HVDC]Project lightning 그룹방

## 그룹방 정보
- **그룹명**: [HVDC]Project lightning
- **정규화명**: HVDC_Project_lightning
- **주제**: HVDC 프로젝트 관련 물류 및 운송 커뮤니케이션
- **참여자**: [참여자 수는 statistics.json 참조]

## 파일 구조
- `original/chat_export.txt` - WhatsApp에서 내보낸 원본 대화 파일
- `output/whatsapp/HVDC_Project_lightning/` - 변환된 JSON 파일들

## 데이터 추출
대화 내용에서 다음 정보가 추출됩니다:
- 선박명 (Vessels)
- 위치 (Locations)
- 시간 정보 (ETA, ETD, ATA, ATD)
- 화물 정보 (Cargo)
- 작업 내용 (Operations)
- 문서 참조 (Documents)
- 장비 정보 (Equipment)
- 수량 정보 (Quantities)

## 변환 명령어
```bash
cd data/whatsapp/HVDC_Project_lightning/original
mrconvert --whatsapp-to-json --extract-entities --entity-csv ../../../csv/Logistics_Entities__Summary_.csv chat_export.txt
```

## 출력 위치
변환 결과는 `output/whatsapp/HVDC_Project_lightning/`에 저장됩니다.
