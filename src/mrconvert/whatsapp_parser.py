"""
WhatsApp 대화 파일을 머신러더블 JSON으로 변환하는 파서 모듈

HVDC 프로젝트 물류 대화 분석을 위한 구조화된 데이터 추출
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from .entity_loader import EntityLoader, get_entity_loader

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageType(Enum):
    """메시지 타입 열거형"""

    TEXT = "text"
    SYSTEM = "system"
    MEDIA = "media"
    EDITED = "edited"


@dataclass
class MessageEntity:
    """메시지에서 추출된 엔티티"""

    vessels: List[str]
    locations: List[str]
    times: Dict[str, str]  # eta, etd, ata, atd
    cargo: List[str]
    operations: List[str]
    documents: List[str]  # 신규
    equipment: List[str]  # 신규
    quantities: List[str]  # 신규
    references: List[str]  # 신규


@dataclass
class WhatsAppMessage:
    """WhatsApp 메시지 데이터 구조"""

    id: int
    timestamp: str
    sender: str
    message_type: MessageType
    content: str
    mentions: List[str]
    entities: MessageEntity
    metadata: Dict[str, Any]


@dataclass
class ConversationMetadata:
    """대화 메타데이터"""

    group_name: str
    created_at: str
    participant_count: int
    date_range: Dict[str, str]
    statistics: Dict[str, Any]


class WhatsAppParser:
    """WhatsApp 대화 파일 파서"""

    def __init__(self, entity_csv_path: str = None):
        # 엔티티 로더 초기화
        self.entity_loader = None
        if entity_csv_path:
            self.entity_loader = get_entity_loader(entity_csv_path)
            self.entity_loader.load_csv(entity_csv_path)

        # 날짜/시간 패턴: YY/M/D AM/PM h:mm
        self.timestamp_pattern = re.compile(
            r"^(\d{2}/\d{1,2}/\d{1,2})\s+(AM|PM)\s+(\d{1,2}:\d{2})"
        )

        # 메시지 패턴: 날짜/시간 - 발신자: 메시지
        self.message_pattern = re.compile(
            r"^(\d{2}/\d{1,2}/\d{1,2})\s+(AM|PM)\s+(\d{1,2}:\d{2})\s+-\s+(.+?):\s+(.+)$"
        )

        # 시스템 메시지 패턴
        self.system_pattern = re.compile(
            r"^(\d{2}/\d{1,2}/\d{1,2})\s+(AM|PM)\s+(\d{1,2}:\d{2})\s+-\s+(.+)$"
        )

        # 멘션 패턴: @⁨사용자⁩
        self.mention_pattern = re.compile(r"@⁨([^⁩]+)⁩")

        # 편집 표시 패턴
        self.edited_pattern = re.compile(r"<This message was edited>")

        # 미디어 파일 패턴
        self.media_pattern = re.compile(r"<미디어 파일 제외됨>")

        # 물류 엔티티 패턴들 - CSV 기반 동적 생성
        self._initialize_entity_patterns()

        self.time_patterns = {
            "eta": re.compile(r"ETA[:\s]+([^,\n]+)", re.IGNORECASE),
            "etd": re.compile(r"ETD[:\s]+([^,\n]+)", re.IGNORECASE),
            "ata": re.compile(r"ATA[:\s]+([^,\n]+)", re.IGNORECASE),
            "atd": re.compile(r"ATD[:\s]+([^,\n]+)", re.IGNORECASE),
        }

        # 기본 패턴들 (CSV가 없을 때 사용)
        self._initialize_fallback_patterns()

    def _initialize_entity_patterns(self):
        """CSV 기반 엔티티 패턴 초기화"""
        if not self.entity_loader:
            return

        # 카테고리별 패턴 생성
        self.vessel_patterns = self.entity_loader.generate_patterns("Vessel")
        self.location_patterns = self.entity_loader.generate_patterns("Site")
        self.operation_patterns = self.entity_loader.generate_patterns("Operation")
        self.document_patterns = self.entity_loader.generate_patterns("Document")
        self.equipment_patterns = self.entity_loader.generate_patterns("Equipment")
        self.quantity_patterns = self.entity_loader.generate_patterns("Quantity")
        self.reference_patterns = self.entity_loader.generate_patterns("Reference")

        # 특수 패턴 추가
        self.vessel_patterns.extend(
            [
                re.compile(r"\b(LCT\s+\w+)\b", re.IGNORECASE),
                re.compile(r"\b(MV\.\s+\w+)\b", re.IGNORECASE),
                re.compile(r"\*([^*]+)\*", re.IGNORECASE),  # *JPT62* 형식 처리
            ]
        )

        # Reference 패턴 (HVDC-* 형식)
        self.reference_patterns.extend(
            [
                re.compile(r"\b(HVDC-[A-Z]+-\d+(?:-\d+)*)\b", re.IGNORECASE),
            ]
        )

    def _initialize_fallback_patterns(self):
        """기본 패턴 초기화 (CSV가 없을 때 사용)"""
        # 기본 선박 패턴
        self.vessel_patterns = [
            re.compile(
                r"\b(JPT\d+|Bushra|Thuraya|Tamara|Razan|Marwah|Jopetwil\s+\d+)\b",
                re.IGNORECASE,
            ),
            re.compile(r"\b(LCT\s+\w+)\b", re.IGNORECASE),
            re.compile(r"\*([^*]+)\*", re.IGNORECASE),
        ]

        # 기본 위치 패턴
        self.location_patterns = [
            re.compile(
                r"\b(DAS|AGI|MOSB|MIRFA|SHU|MIR|JDN|MZP|TBU|MW\d+)\b",
                re.IGNORECASE,
            )
        ]

        # 기본 작업 패턴
        self.operation_patterns = [
            re.compile(
                r"\b(Loading|Offloading|Backloading|RORO|LOLO|anchorage|berth|bunkering|berthing|mooring)\b",
                re.IGNORECASE,
            )
        ]

        # 기본 문서 패턴
        self.document_patterns = [
            re.compile(
                r"\b(BL|CICPA|PL|Manifest|DO|TPI|permit|OSDR|CIPL|HAWB)\b",
                re.IGNORECASE,
            )
        ]

        # 기본 장비 패턴
        self.equipment_patterns = [
            re.compile(
                r"\b(trailer|crane|OT|FR|webbing|CCU|forklift|spreader|HIAB)\b",
                re.IGNORECASE,
            )
        ]

        # 기본 수량 패턴
        self.quantity_patterns = [
            re.compile(r"\b(\d+[Tt]on?|(\d+)\s*[Tt]on?)\b", re.IGNORECASE),
            re.compile(r"\b(\d+mm|(\d+)\s*mm)\b", re.IGNORECASE),
            re.compile(r"\b(\d+[Tt]|(\d+)\s*[Tt])\b", re.IGNORECASE),
        ]

        # 기본 참조 패턴
        self.reference_patterns = [
            re.compile(r"\b(HVDC-[A-Z]+-\d+(?:-\d+)*)\b", re.IGNORECASE),
        ]

    def parse_timestamp(self, date_str: str, time_str: str, ampm: str) -> str:
        """날짜/시간 문자열을 ISO 8601 형식으로 변환"""
        try:
            # 년도 추정 (20xx)
            year = 2000 + int(date_str.split("/")[0])
            month = int(date_str.split("/")[1])
            day = int(date_str.split("/")[2])

            hour = int(time_str.split(":")[0])
            minute = int(time_str.split(":")[1])

            # AM/PM 처리
            if ampm == "PM" and hour != 12:
                hour += 12
            elif ampm == "AM" and hour == 12:
                hour = 0

            dt = datetime(year, month, day, hour, minute)
            return dt.isoformat()
        except Exception as e:
            logger.warning(f"날짜 파싱 오류: {date_str} {time_str} {ampm} - {e}")
            return ""

    def extract_entities(self, content: str) -> MessageEntity:
        """메시지에서 물류 엔티티 추출"""
        vessels = []
        locations = []
        times = {}
        cargo = []
        operations = []
        documents = []
        equipment = []
        quantities = []
        references = []

        # 선박명 추출
        for pattern in self.vessel_patterns:
            matches = pattern.findall(content)
            for match in matches:
                if isinstance(match, str):
                    vessels.append(match)
                elif isinstance(match, tuple):
                    vessels.append(match[0])
                else:
                    vessels.append(str(match))

        # 위치 추출
        for pattern in self.location_patterns:
            matches = pattern.findall(content)
            locations.extend(matches)

        # 시간 정보 추출
        for time_type, pattern in self.time_patterns.items():
            matches = pattern.findall(content)
            if matches:
                times[time_type] = matches[0].strip()

        # 화물 정보 추출 (기존 cargo_patterns 유지)
        if hasattr(self, "cargo_patterns"):
            for pattern in self.cargo_patterns:
                matches = pattern.findall(content)
                cargo.extend(
                    [match if isinstance(match, str) else match[0] for match in matches]
                )

        # 작업 정보 추출
        for pattern in self.operation_patterns:
            matches = pattern.findall(content)
            operations.extend(matches)

        # 문서 정보 추출
        for pattern in self.document_patterns:
            matches = pattern.findall(content)
            documents.extend(matches)

        # 장비 정보 추출
        for pattern in self.equipment_patterns:
            matches = pattern.findall(content)
            equipment.extend(matches)

        # 수량 정보 추출
        for pattern in self.quantity_patterns:
            matches = pattern.findall(content)
            for match in matches:
                if isinstance(match, tuple):
                    quantities.extend([m for m in match if m])
                else:
                    quantities.append(match)

        # 참조번호 추출
        for pattern in self.reference_patterns:
            matches = pattern.findall(content)
            references.extend(matches)

        # 정규화 (엔티티 로더가 있는 경우)
        if self.entity_loader:
            vessels = [self.entity_loader.normalize_entity(v) for v in vessels]
            locations = [self.entity_loader.normalize_entity(l) for l in locations]
            operations = [self.entity_loader.normalize_entity(o) for o in operations]
            documents = [self.entity_loader.normalize_entity(d) for d in documents]
            equipment = [self.entity_loader.normalize_entity(e) for e in equipment]

        return MessageEntity(
            vessels=list(set(vessels)),
            locations=list(set(locations)),
            times=times,
            cargo=list(set(cargo)),
            operations=list(set(operations)),
            documents=list(set(documents)),
            equipment=list(set(equipment)),
            quantities=list(set(quantities)),
            references=list(set(references)),
        )

    def determine_message_type(self, content: str) -> MessageType:
        """메시지 타입 결정"""
        if self.media_pattern.search(content):
            return MessageType.MEDIA
        elif self.edited_pattern.search(content):
            return MessageType.EDITED
        elif any(
            keyword in content.lower()
            for keyword in [
                "그룹을 만들었습니다",
                "그룹에 추가되었습니다",
                "메시지와 통화는",
            ]
        ):
            return MessageType.SYSTEM
        else:
            return MessageType.TEXT

    def parse_message_line(
        self, line: str, line_number: int
    ) -> Optional[WhatsAppMessage]:
        """단일 라인 메시지 파싱"""
        # 일반 메시지 패턴 매칭
        message_match = self.message_pattern.match(line)
        if message_match:
            date_str, ampm, time_str, sender, content = message_match.groups()
            timestamp = self.parse_timestamp(date_str, time_str, ampm)

            # 멘션 추출
            mentions = self.mention_pattern.findall(content)

            # 엔티티 추출
            entities = self.extract_entities(content)

            # 메시지 타입 결정
            message_type = self.determine_message_type(content)

            return WhatsAppMessage(
                id=line_number,
                timestamp=timestamp,
                sender=sender.strip(),
                message_type=message_type,
                content=content.strip(),
                mentions=mentions,
                entities=entities,
                metadata={
                    "is_edited": self.edited_pattern.search(content) is not None,
                    "has_media": self.media_pattern.search(content) is not None,
                    "line_number": line_number,
                },
            )

        # 시스템 메시지 패턴 매칭
        system_match = self.system_pattern.match(line)
        if system_match:
            date_str, ampm, time_str, content = system_match.groups()
            timestamp = self.parse_timestamp(date_str, time_str, ampm)

            return WhatsAppMessage(
                id=line_number,
                timestamp=timestamp,
                sender="System",
                message_type=MessageType.SYSTEM,
                content=content.strip(),
                mentions=[],
                entities=MessageEntity([], [], {}, [], [], [], [], [], []),
                metadata={
                    "is_edited": False,
                    "has_media": False,
                    "line_number": line_number,
                },
            )

        return None

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """WhatsApp 대화 파일 전체 파싱"""
        messages = []
        participants = set()
        vessels = set()
        locations = set()
        cargo_items = set()
        operations = set()

        current_message = None
        line_number = 0
        group_name = "HVDC Project lightning"
        created_at = ""

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line_number += 1
                    line = line.strip()

                    if not line:
                        continue

                    # 메시지 파싱 시도
                    message = self.parse_message_line(line, line_number)

                    if message:
                        # 이전 멀티라인 메시지 처리
                        if current_message:
                            messages.append(current_message)
                            participants.add(current_message.sender)
                            self._update_entities(
                                current_message,
                                vessels,
                                locations,
                                cargo_items,
                                operations,
                            )

                        current_message = message

                        # 그룹 정보 추출
                        if "그룹을 만들었습니다" in message.content:
                            group_name_match = re.search(r'"([^"]+)"', message.content)
                            if group_name_match:
                                group_name = group_name_match.group(1)
                            created_at = message.timestamp

                    else:
                        # 멀티라인 메시지 처리
                        if current_message:
                            current_message.content += " " + line

                    # 진행 상황 로깅
                    if line_number % 1000 == 0:
                        logger.info(f"처리된 라인: {line_number}")

            # 마지막 메시지 처리
            if current_message:
                messages.append(current_message)
                participants.add(current_message.sender)
                self._update_entities(
                    current_message, vessels, locations, cargo_items, operations
                )

        except Exception as e:
            logger.error(f"파일 파싱 오류: {e}")
            raise

        # 통계 생성
        statistics = self._generate_statistics(messages, participants)

        # 날짜 범위 계산
        timestamps = [msg.timestamp for msg in messages if msg.timestamp]
        date_range = {
            "start": min(timestamps) if timestamps else "",
            "end": max(timestamps) if timestamps else "",
        }

        # 대화 메타데이터
        conversation_metadata = ConversationMetadata(
            group_name=group_name,
            created_at=created_at,
            participant_count=len(participants),
            date_range=date_range,
            statistics=statistics,
        )

        # 엔티티 요약
        entities = {
            "participants": sorted(list(participants)),
            "vessels": sorted(list(vessels)),
            "locations": sorted(list(locations)),
            "operations": sorted(list(operations)),
            "cargo": sorted(list(cargo_items)),
        }

        return {
            "conversation": asdict(conversation_metadata),
            "messages": [asdict(msg) for msg in messages],
            "entities": entities,
        }

    def _update_entities(
        self,
        message: WhatsAppMessage,
        vessels: set,
        locations: set,
        cargo_items: set,
        operations: set,
    ):
        """엔티티 세트 업데이트"""
        vessels.update(message.entities.vessels)
        locations.update(message.entities.locations)
        cargo_items.update(message.entities.cargo)
        operations.update(message.entities.operations)

    def _generate_statistics(
        self, messages: List[WhatsAppMessage], participants: set
    ) -> Dict[str, Any]:
        """통계 정보 생성"""
        total_messages = len(messages)
        message_types = {}
        participant_stats = {}

        for message in messages:
            # 메시지 타입별 통계
            msg_type = message.message_type.value
            message_types[msg_type] = message_types.get(msg_type, 0) + 1

            # 참가자별 통계
            sender = message.sender
            if sender not in participant_stats:
                participant_stats[sender] = {
                    "message_count": 0,
                    "vessels_mentioned": set(),
                    "locations_mentioned": set(),
                }

            participant_stats[sender]["message_count"] += 1
            participant_stats[sender]["vessels_mentioned"].update(
                message.entities.vessels
            )
            participant_stats[sender]["locations_mentioned"].update(
                message.entities.locations
            )

        # set을 list로 변환
        for sender in participant_stats:
            participant_stats[sender]["vessels_mentioned"] = list(
                participant_stats[sender]["vessels_mentioned"]
            )
            participant_stats[sender]["locations_mentioned"] = list(
                participant_stats[sender]["locations_mentioned"]
            )

        return {
            "total_messages": total_messages,
            "message_types": message_types,
            "participants": participant_stats,
        }

    def save_to_json(self, data: Dict[str, Any], output_path: str):
        """JSON 파일로 저장"""

        # MessageType 열거형을 문자열로 변환
        def convert_enum(obj):
            if isinstance(obj, MessageType):
                return obj.value
            elif isinstance(obj, MessageEntity):
                return asdict(obj)
            elif isinstance(obj, dict):
                return {k: convert_enum(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_enum(item) for item in obj]
            else:
                return obj

        converted_data = convert_enum(data)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(converted_data, f, ensure_ascii=False, indent=2)
        logger.info(f"JSON 파일 저장 완료: {output_path}")

    def extract_entities_only(self, file_path: str) -> Dict[str, Any]:
        """엔티티만 추출하여 별도 파일로 저장"""
        parsed_data = self.parse_file(file_path)
        entities_data = {
            "conversation_info": parsed_data["conversation"],
            "entities": parsed_data["entities"],
            "statistics": parsed_data["conversation"]["statistics"],
        }
        return entities_data
