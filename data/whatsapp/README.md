# WhatsApp 그룹방 데이터

## 관리 중인 그룹방

1. **HVDC_Project_lightning**
   - 원본명: [HVDC]Project lightning
   - 메시지 수: [statistics.json 참조]
   - 기간: [대화 날짜 범위]
   - 상태: ✅ 활성
   - 폴더: `HVDC_Project_lightning/`

## 폴더 구조
각 그룹방은 다음 구조를 따릅니다:
- `[그룹방명]/original/` - 원본 파일
- `[그룹방명]/README.md` - 그룹방 정보

## 사용법
1. 원본 WhatsApp 대화를 `.txt` 형식으로 내보내기
2. 해당 그룹방 폴더의 `original/` 디렉토리에 저장
3. mrconvert 도구로 JSON 변환:
   ```bash
   cd [그룹방명]/original
   mrconvert --whatsapp-to-json --extract-entities chat_export.txt
   ```
4. 변환 결과는 `output/whatsapp/[그룹방명]/`에 저장됩니다.

## 확장 가능성
새로운 그룹방 추가 시:
1. 그룹방명을 정규화 (특수문자 제거, 공백을 언더스코어로 변경)
2. 동일한 폴더 구조 생성
3. 원본 파일을 `original/` 폴더에 저장
4. README.md 파일 생성
