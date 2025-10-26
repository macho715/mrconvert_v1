"""
Excel 변환기 모듈

Excel 데이터를 다양한 형식으로 변환하는 기능을 제공합니다.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from .excel_parser import ExcelParser, ExcelMetadata
from .excel_validator import ExcelValidator

logger = logging.getLogger(__name__)


class ExcelConverter:
    """Excel 변환기 클래스"""

    def __init__(self):
        """변환기 초기화"""
        self.parser = ExcelParser()
        self.validator = ExcelValidator()

    def convert_excel_file(
        self,
        input_file: str,
        output_dir: str,
        formats: List[str] = ["json", "csv", "md"],
        validate: bool = True,
    ) -> Dict[str, str]:
        """Excel 파일을 다양한 형식으로 변환"""

        logger.info(f"Excel 파일 변환 시작: {input_file}")

        # 출력 디렉토리 생성
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 파일명 생성 (확장자 제거)
        file_stem = Path(input_file).stem

        # Excel 파일 파싱
        df = self.parser.parse_excel_file(input_file)
        self.parser.metadata = self.parser.generate_metadata(input_file)

        # 선적 데이터로 변환
        shipments = self.parser.convert_to_shipments()

        # 데이터 검증
        validation_result = None
        if validate:
            validation_result = self.validator.validate_all_shipments(shipments)
            logger.info(
                f"데이터 검증 완료: {validation_result.statistics['valid_shipments']}/{validation_result.statistics['total_shipments']} 유효"
            )

        # 변환된 파일 경로들
        converted_files = {}

        # JSON 변환
        if "json" in formats:
            json_file = output_path / f"{file_stem}.json"
            self._save_as_json(json_file, shipments, validation_result)
            converted_files["json"] = str(json_file)
            logger.info(f"JSON 파일 생성: {json_file}")

        # CSV 변환
        if "csv" in formats:
            csv_file = output_path / f"{file_stem}.csv"
            self._save_as_csv(csv_file, df)
            converted_files["csv"] = str(csv_file)
            logger.info(f"CSV 파일 생성: {csv_file}")

        # Markdown 변환
        if "md" in formats:
            md_file = output_path / f"{file_stem}.md"
            self._save_as_markdown(md_file, shipments, validation_result)
            converted_files["md"] = str(md_file)
            logger.info(f"Markdown 파일 생성: {md_file}")

        # 검증 리포트
        if validate and validation_result:
            report_file = output_path / f"{file_stem}_validation_report.md"
            self._save_validation_report(report_file, validation_result)
            converted_files["validation_report"] = str(report_file)
            logger.info(f"검증 리포트 생성: {report_file}")

        logger.info(f"Excel 파일 변환 완료: {len(converted_files)}개 파일 생성")
        return converted_files

    def _convert_pandas_types(self, obj):
        """pandas 타입을 JSON 직렬화 가능한 타입으로 변환"""
        import pandas as pd
        import numpy as np

        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif pd.isna(obj):
            return None
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj) if not pd.isna(obj) else None
        elif isinstance(obj, dict):
            return {
                key: self._convert_pandas_types(value) for key, value in obj.items()
            }
        elif isinstance(obj, list):
            return [self._convert_pandas_types(item) for item in obj]
        else:
            return obj

    def _save_as_json(
        self,
        output_file: Path,
        shipments: List[Dict[str, Any]],
        validation_result: Optional[Any] = None,
    ) -> None:
        """JSON 형식으로 저장"""
        # pandas 타입 변환
        converted_shipments = self._convert_pandas_types(shipments)

        output_data = {
            "metadata": {
                "source_file": self.parser.metadata.source_file,
                "total_records": self.parser.metadata.total_records,
                "generated_at": self.parser.metadata.generated_at,
                "schema_version": "1.0",
            },
            "shipments": converted_shipments,
        }

        if validation_result:
            output_data["validation"] = {
                "is_valid": validation_result.is_valid,
                "total_shipments": validation_result.statistics["total_shipments"],
                "valid_shipments": validation_result.statistics["valid_shipments"],
                "error_count": len(validation_result.errors),
                "warning_count": len(validation_result.warnings),
            }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

    def _save_as_csv(self, output_file: Path, df) -> None:
        """CSV 형식으로 저장"""
        df.to_csv(output_file, index=False, encoding="utf-8")

    def _save_as_markdown(
        self,
        output_file: Path,
        shipments: List[Dict[str, Any]],
        validation_result: Optional[Any] = None,
    ) -> None:
        """Markdown 형식으로 저장"""
        md_content = f"""# HVDC STATUS 데이터 변환 결과

## 메타데이터
- **소스 파일**: {self.parser.metadata.source_file}
- **총 레코드 수**: {self.parser.metadata.total_records}
- **생성 일시**: {self.parser.metadata.generated_at}

"""

        if validation_result:
            md_content += f"""## 검증 결과
- **유효한 선적**: {validation_result.statistics['valid_shipments']}/{validation_result.statistics['total_shipments']}
- **오류**: {len(validation_result.errors)}개
- **경고**: {len(validation_result.warnings)}개

"""

        md_content += "## 요약 통계\n\n"

        # 공급업체 통계
        vendors = {}
        for shipment in shipments:
            vendor = shipment.get("vendor", "")
            if vendor:
                vendors[vendor] = vendors.get(vendor, 0) + 1

        md_content += "### 주요 공급업체\n"
        for vendor, count in sorted(vendors.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]:
            md_content += f"- **{vendor}**: {count}건\n"

        md_content += "\n### 컨테이너 타입별 통계\n"

        # 컨테이너 통계
        container_stats = {}
        for shipment in shipments:
            for container_type, count in shipment.get("containers", {}).items():
                if isinstance(count, (int, float)) and count > 0:
                    container_stats[container_type] = (
                        container_stats.get(container_type, 0) + count
                    )

        for container_type, total in container_stats.items():
            md_content += f"- **{container_type}**: {total}개\n"

        md_content += "\n### 주요 선박\n"

        # 선박 통계
        vessels = {}
        for shipment in shipments:
            vessel = shipment.get("vessel_flight_no", "")
            if vessel:
                vessels[vessel] = vessels.get(vessel, 0) + 1

        for vessel, count in sorted(vessels.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]:
            md_content += f"- **{vessel}**: {count}회\n"

        md_content += "\n## 상세 데이터\n\n"
        md_content += "| HVDC CODE | Vendor | Vessel | ETD | ETA | CIF Value |\n"
        md_content += "|-----------|--------|--------|-----|-----|----------|\n"

        for shipment in shipments[:50]:  # 처음 50개만 표시
            etd = shipment.get("logistics", {}).get("etd", "") or ""
            eta = shipment.get("logistics", {}).get("eta", "") or ""
            md_content += f"| {shipment.get('hvdc_code', '')} | {shipment.get('vendor', '')} | {shipment.get('vessel_flight_no', '')} | {etd} | {eta} | {shipment.get('cif_value', 0)} |\n"

        if len(shipments) > 50:
            md_content += f"\n*... 총 {len(shipments)}개 항목 중 50개만 표시*\n"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_content)

    def _save_validation_report(self, output_file: Path, validation_result) -> None:
        """검증 리포트 저장"""
        report_content = self.validator.generate_validation_report(validation_result)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report_content)
