"""
CSV 기반 엔티티 로더

Logistics_Entities_Summary.csv에서 실제 사용된 엔티티 정보를 로드하여
동적 패턴 생성 및 정규화를 지원
"""

import csv
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class EntityInfo:
    """엔티티 정보 데이터 구조"""

    entity: str
    category: str
    count: int
    normalized: str = ""
    variants: List[str] = None

    def __post_init__(self):
        if self.variants is None:
            self.variants = []


class EntityLoader:
    """CSV 파일에서 엔티티 정보를 로드하는 클래스"""

    def __init__(self, csv_path: str = None):
        self.csv_path = csv_path
        self.entities: Dict[str, List[EntityInfo]] = {}
        self.normalization_map: Dict[str, str] = {}
        self.pattern_cache: Dict[str, List[re.Pattern]] = {}

    def load_csv(self, csv_path: str) -> Dict[str, List[EntityInfo]]:
        """CSV 파일에서 엔티티 정보 로드"""
        self.csv_path = csv_path

        if not Path(csv_path).exists():
            logger.error(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
            return {}

        entities_by_category = {}

        try:
            with open(csv_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # 빈 행 건너뛰기
                    if not row.get("Entity") or not row.get("Category"):
                        continue

                    entity = row["Entity"].strip()
                    category = row["Category"].strip()

                    # Count가 없거나 숫자가 아닌 경우 0으로 처리
                    try:
                        count = int(row.get("Count", 0))
                    except ValueError:
                        count = 0

                    entity_info = EntityInfo(
                        entity=entity, category=category, count=count
                    )

                    # 카테고리별로 그룹화
                    if category not in entities_by_category:
                        entities_by_category[category] = []

                    entities_by_category[category].append(entity_info)

                logger.info(
                    f"CSV 로드 완료: {len(entities_by_category)}개 카테고리, "
                    f"{sum(len(entities) for entities in entities_by_category.values())}개 엔티티"
                )

        except Exception as e:
            logger.error(f"CSV 로드 오류: {e}")
            return {}

        # 정규화 및 변형 처리
        self._process_entities(entities_by_category)
        self.entities = entities_by_category

        return entities_by_category

    def _process_entities(self, entities_by_category: Dict[str, List[EntityInfo]]):
        """엔티티 정규화 및 변형 처리"""

        for category, entity_list in entities_by_category.items():
            # 빈도순 정렬
            entity_list.sort(key=lambda x: x.count, reverse=True)

            # 정규화 처리
            for entity_info in entity_list:
                normalized = self._normalize_entity(entity_info.entity, category)
                entity_info.normalized = normalized

                # 변형 생성 (대소문자, 공백 등)
                variants = self._generate_variants(entity_info.entity)
                entity_info.variants = variants

                # 정규화 맵에 추가
                for variant in variants:
                    if variant.lower() not in self.normalization_map:
                        self.normalization_map[variant.lower()] = normalized

    def _normalize_entity(self, entity: str, category: str) -> str:
        """엔티티 정규화"""
        # 카테고리별 정규화 규칙 적용
        if category == "Vessel":
            # 선박명은 첫 글자만 대문자
            return entity.title()
        elif category == "Site":
            # 위치는 대문자로 정규화
            return entity.upper()
        elif category == "Document":
            # 문서는 대문자로 정규화
            return entity.upper()
        elif category == "Equipment":
            # 장비는 첫 글자만 대문자
            return entity.title()
        elif category == "Operation":
            # 작업은 첫 글자만 대문자
            return entity.title()
        elif category == "TimeTag":
            # 시간 태그는 대문자로 정규화
            return entity.upper()
        else:
            # 기본적으로 첫 글자만 대문자
            return entity.title()

    def _generate_variants(self, entity: str) -> List[str]:
        """엔티티 변형 생성"""
        variants = [entity]

        # 대소문자 변형
        variants.extend(
            [entity.upper(), entity.lower(), entity.title(), entity.capitalize()]
        )

        # 공백 제거 변형
        variants.extend(
            [
                entity.replace(" ", ""),
                entity.replace("-", " "),
                entity.replace("_", " "),
            ]
        )

        # 중복 제거 및 원본 순서 유지
        seen = set()
        unique_variants = []
        for variant in variants:
            if variant not in seen:
                seen.add(variant)
                unique_variants.append(variant)

        return unique_variants

    def get_entities_by_category(self, category: str) -> List[EntityInfo]:
        """카테고리별 엔티티 목록 반환"""
        return self.entities.get(category, [])

    def get_top_entities(self, category: str, limit: int = 50) -> List[EntityInfo]:
        """카테고리별 상위 빈도 엔티티 반환"""
        entities = self.get_entities_by_category(category)
        return entities[:limit]

    def generate_patterns(self, category: str) -> List[re.Pattern]:
        """카테고리별 정규식 패턴 생성"""
        if category in self.pattern_cache:
            return self.pattern_cache[category]

        entities = self.get_top_entities(category, 100)  # 상위 100개만 사용

        patterns = []

        for entity_info in entities:
            # 모든 변형에 대한 패턴 생성
            for variant in entity_info.variants:
                if len(variant) < 2:  # 너무 짧은 것은 제외
                    continue

                # 특수문자 이스케이프
                escaped_variant = re.escape(variant)

                # 단어 경계 고려한 패턴
                pattern = rf"\b{escaped_variant}\b"

                try:
                    compiled_pattern = re.compile(pattern, re.IGNORECASE)
                    patterns.append(compiled_pattern)
                except re.error as e:
                    logger.warning(f"패턴 컴파일 오류: {pattern} - {e}")

        self.pattern_cache[category] = patterns
        return patterns

    def normalize_entity(self, entity: str) -> str:
        """엔티티 정규화"""
        return self.normalization_map.get(entity.lower(), entity)

    def get_statistics(self) -> Dict[str, Dict[str, int]]:
        """로드된 엔티티 통계 반환"""
        stats = {}

        for category, entities in self.entities.items():
            total_entities = len(entities)
            total_count = sum(entity.count for entity in entities)
            top_entity = entities[0] if entities else None

            stats[category] = {
                "total_entities": total_entities,
                "total_count": total_count,
                "top_entity": top_entity.entity if top_entity else None,
                "top_count": top_entity.count if top_entity else 0,
            }

        return stats

    def get_validation_data(self) -> Dict[str, Set[str]]:
        """검증용 데이터 반환 (실제 엔티티 목록)"""
        validation_data = {}

        for category, entities in self.entities.items():
            validation_data[category] = set()
            for entity_info in entities:
                validation_data[category].add(entity_info.entity)
                validation_data[category].update(entity_info.variants)

        return validation_data


# 전역 인스턴스 (성능 최적화)
_entity_loader = None


def get_entity_loader(csv_path: str = None) -> EntityLoader:
    """엔티티 로더 싱글톤 인스턴스 반환"""
    global _entity_loader

    if _entity_loader is None or (csv_path and _entity_loader.csv_path != csv_path):
        _entity_loader = EntityLoader(csv_path)
        if csv_path:
            _entity_loader.load_csv(csv_path)

    return _entity_loader


def load_entities_from_csv(csv_path: str) -> Dict[str, List[EntityInfo]]:
    """CSV에서 엔티티 로드 (편의 함수)"""
    loader = get_entity_loader(csv_path)
    return loader.load_csv(csv_path)
