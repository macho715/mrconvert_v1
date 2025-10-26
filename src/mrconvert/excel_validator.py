"""
Excel 데이터 검증 모듈

Excel 파싱 결과의 데이터 무결성을 검증하는 기능을 제공합니다.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """검증 결과"""

    is_valid: bool
    errors: List[str]
    warnings: List[str]
    statistics: Dict[str, Any]


class ExcelValidator:
    """Excel 데이터 검증기"""

    def __init__(self):
        """검증기 초기화"""
        self.hvdc_code_pattern = re.compile(r"^HVDC-[A-Z]+-\d+$")
        self.date_patterns = [
            re.compile(r"^\d{4}-\d{2}-\d{2}$"),  # YYYY-MM-DD
            re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"),  # ISO format
        ]

    def validate_hvdc_code(self, code: str) -> bool:
        """HVDC 코드 형식 검증"""
        if not code or code == "":
            return False
        return bool(self.hvdc_code_pattern.match(code))

    def validate_date_format(self, date_str: str) -> bool:
        """날짜 형식 검증"""
        if not date_str or date_str == "":
            return True  # 빈 날짜는 허용

        for pattern in self.date_patterns:
            if pattern.match(date_str):
                return True
        return False

    def validate_numeric_value(
        self, value: Any, field_name: str
    ) -> Tuple[bool, Optional[str]]:
        """숫자 값 검증"""
        import pandas as pd
        import numpy as np

        if pd.isna(value) or value == "":
            return True, None  # 빈 값은 허용

        try:
            # numpy 배열이나 pandas Series인 경우 처리
            if isinstance(value, (np.ndarray, pd.Series)):
                if len(value) == 1:
                    value = value[0]
                else:
                    return False, f"{field_name}: 배열 값은 단일 값이어야 합니다"

            float_value = float(value)
            if float_value < 0:
                return False, f"{field_name}: 음수 값이 허용되지 않습니다"
            return True, None
        except (ValueError, TypeError):
            return False, f"{field_name}: 숫자 형식이 올바르지 않습니다"

    def validate_currency_code(self, currency: str) -> bool:
        """통화 코드 검증"""
        if not currency or currency == "":
            return True  # 빈 값은 허용

        valid_currencies = ["USD", "EUR", "AED", "KRW", "JPY", "CNY"]
        return currency.upper() in valid_currencies

    def validate_incoterms(self, incoterms: str) -> bool:
        """인코텀즈 검증"""
        if not incoterms or incoterms == "":
            return True  # 빈 값은 허용

        valid_incoterms = [
            "CIF",
            "FOB",
            "EXW",
            "FCA",
            "CPT",
            "CIP",
            "DAP",
            "DPU",
            "DDP",
        ]
        return incoterms.upper() in valid_incoterms

    def validate_shipment_data(self, shipment: Dict[str, Any]) -> ValidationResult:
        """선적 데이터 검증"""
        errors = []
        warnings = []

        # 필수 필드 검증
        required_fields = ["hvdc_code", "vendor", "currency"]
        for field in required_fields:
            if not shipment.get(field) or shipment.get(field) == "":
                errors.append(f"필수 필드 누락: {field}")

        # HVDC 코드 형식 검증
        hvdc_code = shipment.get("hvdc_code", "")
        if hvdc_code and not self.validate_hvdc_code(hvdc_code):
            errors.append(f"잘못된 HVDC 코드 형식: {hvdc_code}")

        # 날짜 형식 검증
        date_fields = ["invoice_date", "etd", "atd", "eta", "ata"]
        for field in date_fields:
            date_value = shipment.get(field)
            if date_value and not self.validate_date_format(date_value):
                warnings.append(f"날짜 형식이 표준화되지 않음: {field} = {date_value}")

        # 금액 필드 검증
        amount_fields = ["invoice_value", "freight", "insurance", "cif_value"]
        for field in amount_fields:
            value = shipment.get(field)
            is_valid, error_msg = self.validate_numeric_value(value, field)
            if not is_valid:
                errors.append(error_msg)
            elif value and value > 0:
                # 금액 일관성 검증
                if (
                    field == "cif_value"
                    and shipment.get("invoice_value")
                    and shipment.get("freight")
                    and shipment.get("insurance")
                ):
                    expected_cif = (
                        shipment.get("invoice_value", 0)
                        + shipment.get("freight", 0)
                        + shipment.get("insurance", 0)
                    )
                    if abs(float(value) - expected_cif) > 0.01:  # 소수점 오차 허용
                        warnings.append(
                            f"CIF 값이 일치하지 않음: 계산값 {expected_cif} vs 입력값 {value}"
                        )

        # 통화 코드 검증
        currency = shipment.get("currency", "")
        if currency and not self.validate_currency_code(currency):
            warnings.append(f"알 수 없는 통화 코드: {currency}")

        # 인코텀즈 검증
        incoterms = shipment.get("incoterms", "")
        if incoterms and not self.validate_incoterms(incoterms):
            warnings.append(f"알 수 없는 인코텀즈: {incoterms}")

        # 컨테이너 수량 검증
        containers = shipment.get("containers", {})
        for container_type, count in containers.items():
            if count and isinstance(count, (int, float)) and count < 0:
                errors.append(f"컨테이너 수량이 음수: {container_type} = {count}")

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings, statistics={}
        )

    def validate_all_shipments(
        self, shipments: List[Dict[str, Any]]
    ) -> ValidationResult:
        """전체 선적 데이터 검증"""
        all_errors = []
        all_warnings = []
        statistics = {
            "total_shipments": len(shipments),
            "valid_shipments": 0,
            "invalid_shipments": 0,
            "warning_shipments": 0,
            "hvdc_codes": set(),
            "vendors": set(),
            "vessels": set(),
            "total_invoice_value": 0,
            "total_cif_value": 0,
            "container_counts": {},
        }

        for idx, shipment in enumerate(shipments):
            result = self.validate_shipment_data(shipment)

            if result.is_valid:
                statistics["valid_shipments"] += 1
            else:
                statistics["invalid_shipments"] += 1
                all_errors.extend([f"행 {idx + 1}: {error}" for error in result.errors])

            if result.warnings:
                statistics["warning_shipments"] += 1
                all_warnings.extend(
                    [f"행 {idx + 1}: {warning}" for warning in result.warnings]
                )

            # 통계 수집
            if shipment.get("hvdc_code"):
                statistics["hvdc_codes"].add(shipment["hvdc_code"])
            if shipment.get("vendor"):
                statistics["vendors"].add(shipment["vendor"])
            if shipment.get("vessel_flight_no"):
                statistics["vessels"].add(shipment["vessel_flight_no"])

            if shipment.get("invoice_value"):
                statistics["total_invoice_value"] += float(shipment["invoice_value"])
            if shipment.get("cif_value"):
                statistics["total_cif_value"] += float(shipment["cif_value"])

            # 컨테이너 통계
            containers = shipment.get("containers", {})
            for container_type, count in containers.items():
                if isinstance(count, (int, float)) and count > 0:
                    statistics["container_counts"][container_type] = (
                        statistics["container_counts"].get(container_type, 0) + count
                    )

        # 통계 정리
        statistics["unique_hvdc_codes"] = len(statistics["hvdc_codes"])
        statistics["unique_vendors"] = len(statistics["vendors"])
        statistics["unique_vessels"] = len(statistics["vessels"])

        return ValidationResult(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings,
            statistics=statistics,
        )

    def generate_validation_report(self, validation_result: ValidationResult) -> str:
        """검증 리포트 생성"""
        report = "# Excel 데이터 검증 리포트\n\n"

        report += "## 검증 결과 요약\n"
        report += (
            f"- **전체 선적 수**: {validation_result.statistics['total_shipments']}\n"
        )
        report += (
            f"- **유효한 선적**: {validation_result.statistics['valid_shipments']}\n"
        )
        report += f"- **오류가 있는 선적**: {validation_result.statistics['invalid_shipments']}\n"
        report += f"- **경고가 있는 선적**: {validation_result.statistics['warning_shipments']}\n\n"

        report += "## 데이터 통계\n"
        report += f"- **고유 HVDC 코드**: {validation_result.statistics['unique_hvdc_codes']}\n"
        report += (
            f"- **고유 공급업체**: {validation_result.statistics['unique_vendors']}\n"
        )
        report += f"- **고유 선박**: {validation_result.statistics['unique_vessels']}\n"
        report += f"- **총 송장 금액**: ${validation_result.statistics['total_invoice_value']:,.2f}\n"
        report += f"- **총 CIF 금액**: ${validation_result.statistics['total_cif_value']:,.2f}\n\n"

        if validation_result.statistics["container_counts"]:
            report += "## 컨테이너 통계\n"
            for container_type, count in validation_result.statistics[
                "container_counts"
            ].items():
                report += f"- **{container_type}**: {count}개\n"
            report += "\n"

        if validation_result.errors:
            report += "## 오류 목록\n"
            for error in validation_result.errors[:20]:  # 처음 20개만 표시
                report += f"- {error}\n"
            if len(validation_result.errors) > 20:
                report += (
                    f"... 총 {len(validation_result.errors)}개 오류 중 20개만 표시\n"
                )
            report += "\n"

        if validation_result.warnings:
            report += "## 경고 목록\n"
            for warning in validation_result.warnings[:20]:  # 처음 20개만 표시
                report += f"- {warning}\n"
            if len(validation_result.warnings) > 20:
                report += (
                    f"... 총 {len(validation_result.warnings)}개 경고 중 20개만 표시\n"
                )
            report += "\n"

        return report


# pandas import 추가
import pandas as pd
