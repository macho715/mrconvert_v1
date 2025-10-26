"""
HVDC Excel 파일 파서 모듈

Excel 파일을 머신러더블 형식으로 변환하는 기능을 제공합니다.
"""

import pandas as pd
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class ShipmentData:
    """선적 데이터 구조"""

    no: int
    hvdc_code: str
    mr_number: str
    commercial_invoice_no: str
    invoice_date: str
    po_number: str
    vendor: str
    category: str
    main_description: str
    sub_description: str
    incoterms: str
    currency: str
    invoice_value: float
    freight: float
    insurance: float
    cif_value: float
    coe: str
    pol: str
    pod: str
    bl_awb_no: str
    vessel_flight_no: str
    vessel_imo_no: str
    shipping_line: str
    forwarder: str
    ship_mode: str
    pkg: int
    containers: Dict[str, Any]
    quantities: Dict[str, Any]
    logistics: Dict[str, Any]
    customs: Dict[str, Any]
    delivery: Dict[str, Any]


@dataclass
class ExcelMetadata:
    """Excel 파일 메타데이터"""

    source_file: str
    sheet_name: str
    total_records: int
    generated_at: str
    columns: List[str]
    data_types: Dict[str, str]


class ExcelParser:
    """Excel 파일 파서 클래스"""

    def __init__(self):
        """파서 초기화"""
        self.data: Optional[pd.DataFrame] = None
        self.metadata: Optional[ExcelMetadata] = None

    def normalize_column_name(self, column: str) -> str:
        """컬럼명 정규화"""
        # 공백 제거 및 언더스코어로 변환
        normalized = re.sub(r"\s+", "_", column.strip())
        # 특수문자 제거
        normalized = re.sub(r"[^\w_]", "", normalized)
        # 소문자 변환
        return normalized.lower()

    def normalize_date(self, date_value: Any) -> str:
        """날짜 정규화 (ISO 8601 형식)"""
        if pd.isna(date_value) or date_value == "":
            return None

        if isinstance(date_value, str):
            try:
                # 다양한 날짜 형식 시도
                for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"]:
                    try:
                        dt = datetime.strptime(date_value, fmt)
                        return dt.isoformat()
                    except ValueError:
                        continue
                return date_value
            except:
                return date_value

        if isinstance(date_value, (datetime, pd.Timestamp)):
            return date_value.isoformat()

        return str(date_value)

    def extract_containers(self, row: pd.Series) -> Dict[str, Any]:
        """컨테이너 정보 추출"""
        container_cols = [
            "20dc",
            "40dc",
            "40hq",
            "45hq",
            "20ot(in)",
            "20ot(oh)",
            "40ot(in)",
            "40ot(oh)",
            "20fr(in)",
            "40fr(in)",
            "20fr(fv)",
            "40fr(ow)",
            "20fr(ow,oh)",
            "40fr(ow,oh)",
            "40fr(ow,ol)",
            "lcl",
        ]

        containers = {}
        for col in container_cols:
            if col in row and pd.notna(row[col]):
                containers[col] = (
                    float(row[col]) if isinstance(row[col], (int, float)) else row[col]
                )

        return containers

    def extract_quantities(self, row: pd.Series) -> Dict[str, Any]:
        """수량 정보 추출"""
        quantity_cols = [
            "qty_of_cntr",
            "g_bulk",
            "o_bulk",
            "h_bulk",
            "gwt_(kg)",
            "cbm",
            "r/t_(grand-_total)",
            "a_cwt(kg)",
        ]

        quantities = {}
        for col in quantity_cols:
            if col in row and pd.notna(row[col]):
                quantities[col] = (
                    float(row[col]) if isinstance(row[col], (int, float)) else row[col]
                )

        return quantities

    def extract_logistics(self, row: pd.Series) -> Dict[str, Any]:
        """물류 정보 추출"""
        logistics_cols = [
            "etd",
            "atd",
            "eta",
            "ata",
            "attestation_date",
            "do_collection",
            "customs_start",
            "customs_close",
            "custom_code",
        ]

        logistics = {}
        for col in logistics_cols:
            if col in row and pd.notna(row[col]):
                logistics[col] = self.normalize_date(row[col])

        return logistics

    def extract_customs(self, row: pd.Series) -> Dict[str, Any]:
        """세관 정보 추출"""
        customs_cols = ["duty_amt_(aed)", "vat_amt_(aed)"]

        customs = {}
        for col in customs_cols:
            if col in row and pd.notna(row[col]):
                customs[col] = (
                    float(row[col]) if isinstance(row[col], (int, float)) else row[col]
                )

        return customs

    def extract_delivery(self, row: pd.Series) -> Dict[str, Any]:
        """배송 정보 추출"""
        delivery_cols = [
            "shu",
            "mir",
            "das",
            "agi",
            "dsv_indoor",
            "dsv_outdoor",
            "dsv_mzd",
            "jdn_mzd",
            "jdn_waterfront",
            "mosb",
            "aaa_storage",
            "zener_(wh)",
            "hauler",
            "dg_storage",
            "vijay_tanks",
            "delivery_date",
        ]

        delivery = {}
        for col in delivery_cols:
            if col in row and pd.notna(row[col]):
                if "date" in col.lower():
                    delivery[col] = self.normalize_date(row[col])
                else:
                    delivery[col] = row[col]

        return delivery

    def parse_excel_file(self, file_path: str) -> pd.DataFrame:
        """Excel 파일 파싱"""
        try:
            logger.info(f"Excel 파일 읽기 시작: {file_path}")

            # Excel 파일 읽기
            df = pd.read_excel(file_path, sheet_name=0)

            # 컬럼명 정규화
            df.columns = [self.normalize_column_name(col) for col in df.columns]

            logger.info(
                f"Excel 파일 읽기 완료: {len(df)}개 행, {len(df.columns)}개 컬럼"
            )

            self.data = df
            return df

        except Exception as e:
            logger.error(f"Excel 파일 읽기 실패: {e}")
            raise

    def generate_metadata(self, file_path: str) -> ExcelMetadata:
        """메타데이터 생성"""
        if self.data is None:
            raise ValueError(
                "데이터가 로드되지 않았습니다. parse_excel_file을 먼저 호출하세요."
            )

        return ExcelMetadata(
            source_file=file_path,
            sheet_name="시트1",
            total_records=len(self.data),
            generated_at=datetime.now().isoformat(),
            columns=list(self.data.columns),
            data_types={col: str(dtype) for col, dtype in self.data.dtypes.items()},
        )

    def convert_to_shipments(self) -> List[Dict[str, Any]]:
        """데이터를 선적 정보로 변환"""
        if self.data is None:
            raise ValueError("데이터가 로드되지 않았습니다.")

        shipments = []

        for idx, row in self.data.iterrows():
            try:
                shipment = {
                    "no": (
                        int(row.get("no", idx + 1))
                        if pd.notna(row.get("no"))
                        else idx + 1
                    ),
                    "hvdc_code": str(row.get("hvdc_code", "")),
                    "mr_number": str(row.get("mr#", "")),
                    "commercial_invoice_no": str(row.get("commercial_invoice_no.", "")),
                    "invoice_date": self.normalize_date(row.get("invoice_date")),
                    "po_number": str(row.get("po_no.", "")),
                    "vendor": str(row.get("vendor", "")),
                    "category": str(row.get("category", "")),
                    "main_description": str(row.get("main_description_(po)", "")),
                    "sub_description": str(row.get("sub_description", "")),
                    "incoterms": str(row.get("incoterms", "")),
                    "currency": str(row.get("currency", "")),
                    "invoice_value": (
                        float(row.get("invoice_value\n_(a)", 0))
                        if pd.notna(row.get("invoice_value\n_(a)"))
                        else 0
                    ),
                    "freight": (
                        float(row.get("freight\n_(b)", 0))
                        if pd.notna(row.get("freight\n_(b)"))
                        else 0
                    ),
                    "insurance": (
                        float(row.get("insurance\n_(c)", 0))
                        if pd.notna(row.get("insurance\n_(c)"))
                        else 0
                    ),
                    "cif_value": (
                        float(row.get("cif_value\n_(a+b+c)", 0))
                        if pd.notna(row.get("cif_value\n_(a+b+c)"))
                        else 0
                    ),
                    "coe": str(row.get("coe", "")),
                    "pol": str(row.get("pol", "")),
                    "pod": str(row.get("pod", "")),
                    "bl_awb_no": str(row.get("b/l_no./\n_awb_no.", "")),
                    "vessel_flight_no": str(row.get("vessel_name/\n_flight_no.", "")),
                    "vessel_imo_no": str(row.get("vessel_imo_no.", "")),
                    "shipping_line": str(row.get("shipping_line", "")),
                    "forwarder": str(row.get("forwarder", "")),
                    "ship_mode": str(row.get("ship\n_mode", "")),
                    "pkg": int(row.get("pkg", 0)) if pd.notna(row.get("pkg")) else 0,
                    "containers": self.extract_containers(row),
                    "quantities": self.extract_quantities(row),
                    "logistics": self.extract_logistics(row),
                    "customs": self.extract_customs(row),
                    "delivery": self.extract_delivery(row),
                }
                shipments.append(shipment)

            except Exception as e:
                logger.warning(f"행 {idx} 처리 중 오류: {e}")
                continue

        logger.info(f"선적 데이터 변환 완료: {len(shipments)}개 항목")
        return shipments

    def _convert_pandas_types(self, obj):
        """pandas 타입을 JSON 직렬화 가능한 타입으로 변환"""
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

    def save_to_json(self, output_path: str, shipments: List[Dict[str, Any]]) -> None:
        """JSON 파일로 저장"""
        # pandas 타입 변환
        converted_shipments = self._convert_pandas_types(shipments)

        output_data = {
            "metadata": self._convert_pandas_types(asdict(self.metadata)),
            "shipments": converted_shipments,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        logger.info(f"JSON 파일 저장 완료: {output_path}")

    def save_to_csv(self, output_path: str) -> None:
        """CSV 파일로 저장"""
        if self.data is None:
            raise ValueError("데이터가 로드되지 않았습니다.")

        self.data.to_csv(output_path, index=False, encoding="utf-8")
        logger.info(f"CSV 파일 저장 완료: {output_path}")

    def save_to_markdown(
        self, output_path: str, shipments: List[Dict[str, Any]]
    ) -> None:
        """Markdown 파일로 저장"""
        md_content = f"""# HVDC STATUS 데이터 변환 결과

## 메타데이터
- **소스 파일**: {self.metadata.source_file}
- **총 레코드 수**: {self.metadata.total_records}
- **생성 일시**: {self.metadata.generated_at}

## 요약 통계

### 컨테이너 타입별 통계
"""

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
            md_content += f"| {shipment.get('hvdc_code', '')} | {shipment.get('vendor', '')} | {shipment.get('vessel_flight_no', '')} | {shipment.get('logistics', {}).get('etd', '')} | {shipment.get('logistics', {}).get('eta', '')} | {shipment.get('cif_value', 0)} |\n"

        if len(shipments) > 50:
            md_content += f"\n*... 총 {len(shipments)}개 항목 중 50개만 표시*\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        logger.info(f"Markdown 파일 저장 완료: {output_path}")
