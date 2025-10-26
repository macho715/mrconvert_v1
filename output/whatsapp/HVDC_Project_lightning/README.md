# [HVDC]Project lightning - 변환 결과

## 파일 설명

### 1. conversation.json
전체 대화 내용을 구조화한 JSON 파일
```json
{
  "metadata": {
    "group_name": "[HVDC]Project lightning",
    "total_messages": 1234,
    "date_range": "2024-XX-XX to 2024-XX-XX",
    "participants": ["User1", "User2", ...]
  },
  "messages": [
    {
      "timestamp": "24/1/15 PM 2:30",
      "sender": "User Name",
      "content": "Message content",
      "type": "text|media|system",
      "entities": {...}
    }
  ]
}
```

### 2. entities.json
추출된 물류 엔티티 정보
```json
{
  "vessels": ["JPT71", "JPT62", ...],
  "locations": ["Jubail", "Dammam", ...],
  "times": {
    "eta": ["2024-01-15", ...],
    "etd": ["2024-01-16", ...]
  },
  "cargo": ["containers", "bulk cargo", ...],
  "operations": ["loading", "discharging", ...],
  "documents": ["B/L", "Invoice", ...],
  "equipment": ["crane", "forklift", ...],
  "quantities": ["20 containers", "500 tons", ...]
}
```

### 3. statistics.json
대화 통계 정보
```json
{
  "total_messages": 1234,
  "participants": {
    "User1": 456,
    "User2": 789
  },
  "message_types": {
    "text": 1000,
    "media": 200,
    "system": 34
  },
  "activity_by_hour": {...},
  "most_active_day": "2024-01-15"
}
```

## 생성 정보
- **원본**: `data/whatsapp/HVDC_Project_lightning/original/chat_export.txt`
- **도구**: mrconvert WhatsApp Parser v1.0
- **엔티티 참조**: `data/csv/Logistics_Entities__Summary_.csv`
- **생성일**: 2025-10-23
