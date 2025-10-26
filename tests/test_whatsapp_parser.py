"""
WhatsApp 파서 테스트 모듈

HVDC 프로젝트 물류 대화 분석을 위한 파서 기능 테스트
"""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime

from mrconvert.whatsapp_parser import (
    WhatsAppParser,
    MessageType,
    WhatsAppMessage,
    MessageEntity,
)


class TestWhatsAppParser:
    """WhatsApp 파서 테스트 클래스"""

    def setup_method(self):
        """테스트 설정"""
        self.parser = WhatsAppParser()

    def test_parse_timestamp(self):
        """날짜/시간 파싱 테스트"""
        # 정상적인 날짜/시간
        timestamp = self.parser.parse_timestamp("24/8/22", "9:30", "AM")
        assert timestamp == "2024-08-22T09:30:00"

        timestamp = self.parser.parse_timestamp("24/8/22", "3:45", "PM")
        assert timestamp == "2024-08-22T15:45:00"

        # 자정 처리
        timestamp = self.parser.parse_timestamp("24/8/22", "12:00", "AM")
        assert timestamp == "2024-08-22T00:00:00"

        # 정오 처리
        timestamp = self.parser.parse_timestamp("24/8/22", "12:00", "PM")
        assert timestamp == "2024-08-22T12:00:00"

    def test_extract_entities(self):
        """엔티티 추출 테스트"""
        content = "JPT62 eta DAS tomorrow 9am, loading containers and porta cabins"
        entities = self.parser.extract_entities(content)

        assert "JPT62" in entities.vessels
        assert "DAS" in entities.locations
        assert "containers" in entities.cargo
        assert "porta cabins" in entities.cargo
        assert "loading" in entities.operations

    def test_determine_message_type(self):
        """메시지 타입 결정 테스트"""
        # 일반 텍스트 메시지
        msg_type = self.parser.determine_message_type("Hello world")
        assert msg_type == MessageType.TEXT

        # 미디어 메시지
        msg_type = self.parser.determine_message_type("사진 <미디어 파일 제외됨>")
        assert msg_type == MessageType.MEDIA

        # 편집된 메시지
        msg_type = self.parser.determine_message_type(
            "Updated message <This message was edited>"
        )
        assert msg_type == MessageType.EDITED

        # 시스템 메시지
        msg_type = self.parser.determine_message_type("그룹을 만들었습니다")
        assert msg_type == MessageType.SYSTEM

    def test_parse_message_line(self):
        """메시지 라인 파싱 테스트"""
        line = "24/8/22 AM 9:30 - Haitham: JPT62 eta DAS tomorrow 9am"
        message = self.parser.parse_message_line(line, 1)

        assert message is not None
        assert message.sender == "Haitham"
        assert message.timestamp == "2024-08-22T09:30:00"
        assert message.content == "JPT62 eta DAS tomorrow 9am"
        assert "JPT62" in message.entities.vessels
        assert "DAS" in message.entities.locations

    def test_parse_system_message(self):
        """시스템 메시지 파싱 테스트"""
        line = '22/11/15 AM 11:20 - +971 56 338 5629님이 "[HVDC]Project lightning🤗"그룹을 만들었습니다'
        message = self.parser.parse_message_line(line, 1)

        assert message is not None
        assert message.sender == "System"
        assert message.message_type == MessageType.SYSTEM
        assert "그룹을 만들었습니다" in message.content

    def test_parse_file_small(self):
        """소규모 파일 파싱 테스트"""
        test_content = """24/8/21 PM 1:28 - 메시지와 통화는 종단간 암호화되어 안전하게 보호됩니다. 이 대화에 참여한 사람만 이러한 메시지와 통화를 읽거나 듣거나 공유할 수 있습니다. 더 알아보기.
22/11/15 AM 11:20 - +971 56 338 5629님이 "[HVDC]Project lightning🤗"그룹을 만들었습니다
24/8/21 PM 2:38 - kEn 🏄🏻🌊: Mr. Cha email - minkyu.cha@samsung.com
24/8/21 PM 9:50 - Haitham: Tamarah eta das 15:00 tomorrow <This message was edited>
24/8/21 PM 9:50 - Haitham: Thuraya eta mosb 9am
24/8/21 PM 9:50 - Shariff: Noted"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(test_content)
            temp_path = f.name

        try:
            result = self.parser.parse_file(temp_path)

            # 기본 구조 확인
            assert "conversation" in result
            assert "messages" in result
            assert "entities" in result

            # 메시지 수 확인
            assert len(result["messages"]) == 6

            # 그룹 정보 확인
            assert "[HVDC]Project lightning🤗" in result["conversation"]["group_name"]

            # 엔티티 확인
            assert "Tamarah" in result["entities"]["vessels"]
            assert "Thuraya" in result["entities"]["vessels"]
            assert "DAS" in result["entities"]["locations"]
            assert "MOSB" in result["entities"]["locations"]

        finally:
            Path(temp_path).unlink()

    def test_multiline_message_parsing(self):
        """멀티라인 메시지 파싱 테스트"""
        test_content = """24/8/22 AM 9:28 - Eddel Jose: Good Morning Sir...
HITACHI Material delivery received on site (MIRFA SITE) - 2 TRAILERS
HVDC-ADOPT-HE-0149 &
HVDC-ADOPT-HE-0151
ATA: 0815HRS
UNLOADING COMPLETED: 0920HRS"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(test_content)
            temp_path = f.name

        try:
            result = self.parser.parse_file(temp_path)

            # 단일 메시지로 파싱되어야 함
            assert len(result["messages"]) == 1

            message = result["messages"][0]
            assert message["sender"] == "Eddel Jose"
            assert "HITACHI Material delivery" in message["content"]
            assert "HVDC-ADOPT-HE-0149" in message["content"]
            assert "HVDC-ADOPT-HE-0151" in message["content"]
            assert "ATA: 0815HRS" in message["content"]
            assert "UNLOADING COMPLETED: 0920HRS" in message["content"]

        finally:
            Path(temp_path).unlink()

    def test_entity_extraction_comprehensive(self):
        """포괄적인 엔티티 추출 테스트"""
        test_content = """24/8/25 AM 7:24 - Haitham: *JPT62* at underway to agi eta 15:00hrs

*JPT71* at MW4 to load aggregate for agi

*Bushra* underway  to das eta 9am

*Thuraya* at das offloading for us.
24/8/25 AM 7:34 - Ramaju Das: Today Backloading Plan
40' x 01 Container empty
40' x 02 HHO Basket empty
20' x 01 container with General waste
20' x 01 HHO Basket with wood waste
20' x 01 HHO Basket Empty
28' x 04 HHO Basket Empty (ALT)
Vessel : TBU"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(test_content)
            temp_path = f.name

        try:
            result = self.parser.parse_file(temp_path)

            # 선박 엔티티 확인
            vessels = result["entities"]["vessels"]
            expected_vessels = ["JPT62", "JPT71", "Bushra", "Thuraya", "TBU"]
            for vessel in expected_vessels:
                assert vessel in vessels

            # 위치 엔티티 확인
            locations = result["entities"]["locations"]
            expected_locations = ["AGI", "MW4", "DAS"]
            for location in expected_locations:
                assert location in locations

            # 화물 엔티티 확인
            cargo = result["entities"]["cargo"]
            expected_cargo = ["Container", "Basket"]
            for cargo_item in expected_cargo:
                assert cargo_item in cargo

            # 작업 엔티티 확인
            operations = result["entities"]["operations"]
            expected_operations = ["Loading", "Offloading", "Backloading"]
            for operation in expected_operations:
                assert operation in operations

        finally:
            Path(temp_path).unlink()

    def test_mention_extraction(self):
        """멘션 추출 테스트"""
        test_content = """24/8/23 AM 7:36 - 국일 Kim: @⁨Ramaju Das⁩ BL shipment No
4 X AVE W.SKIP
830
834
804
797
24/8/23 AM 7:37 - 국일 Kim: update the departure notification"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(test_content)
            temp_path = f.name

        try:
            result = self.parser.parse_file(temp_path)

            # 첫 번째 메시지에서 멘션 확인
            first_message = result["messages"][0]
            assert "Ramaju Das" in first_message["mentions"]

        finally:
            Path(temp_path).unlink()

    def test_statistics_generation(self):
        """통계 생성 테스트"""
        test_content = """24/8/21 PM 2:38 - kEn 🏄🏻🌊: Mr. Cha email - minkyu.cha@samsung.com
24/8/21 PM 9:50 - Haitham: Tamarah eta das 15:00 tomorrow <This message was edited>
24/8/21 PM 9:50 - Haitham: Thuraya eta mosb 9am
24/8/21 PM 9:50 - Shariff: Noted
24/8/21 PM 9:51 - Ramaju Das: Ok noted"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(test_content)
            temp_path = f.name

        try:
            result = self.parser.parse_file(temp_path)

            # 통계 확인
            stats = result["conversation"]["statistics"]
            assert stats["total_messages"] == 5
            assert len(stats["participants"]) == 4

            # 참가자별 메시지 수 확인
            participants = stats["participants"]
            assert participants["kEn 🏄🏻🌊"]["message_count"] == 1
            assert participants["Haitham"]["message_count"] == 2
            assert participants["Shariff"]["message_count"] == 1
            assert participants["Ramaju Das"]["message_count"] == 1

        finally:
            Path(temp_path).unlink()

    def test_json_output_structure(self):
        """JSON 출력 구조 테스트"""
        test_content = """24/8/21 PM 2:38 - kEn 🏄🏻🌊: Mr. Cha email - minkyu.cha@samsung.com
24/8/21 PM 9:50 - Haitham: JPT62 eta DAS 15:00"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(test_content)
            temp_path = f.name

        try:
            result = self.parser.parse_file(temp_path)

            # JSON 구조 확인
            assert isinstance(result, dict)
            assert "conversation" in result
            assert "messages" in result
            assert "entities" in result

            # 대화 메타데이터 구조 확인
            conversation = result["conversation"]
            assert "group_name" in conversation
            assert "created_at" in conversation
            assert "participant_count" in conversation
            assert "date_range" in conversation
            assert "statistics" in conversation

            # 메시지 구조 확인
            message = result["messages"][0]
            assert "id" in message
            assert "timestamp" in message
            assert "sender" in message
            assert "message_type" in message
            assert "content" in message
            assert "mentions" in message
            assert "entities" in message
            assert "metadata" in message

        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    pytest.main([__file__])
