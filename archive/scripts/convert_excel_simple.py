"""
간단한 Excel 변환 스크립트
"""

import pandas as pd
import json
from pathlib import Path


def convert_pandas_types(obj):
    """pandas 타입을 JSON 직렬화 가능한 타입으로 변환"""
    if pd.isna(obj):
        return None
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, (int, float)):
        return float(obj) if not pd.isna(obj) else None
    else:
        return str(obj)


def structure_shipment_data(row):
    """행 데이터를 구조화된 선적 정보로 변환"""
    return {
        "hvdc_code": convert_pandas_types(row.get("hvdc_code", "")),
        "basic_info": {
            "no": convert_pandas_types(row.get("no")),
            "mr_number": convert_pandas_types(row.get("mr#")),
            "commercial_invoice_no": convert_pandas_types(
                row.get("commercial_invoice_no.")
            ),
            "invoice_date": convert_pandas_types(row.get("invoice_date")),
            "po_number": convert_pandas_types(row.get("po_no.")),
            "vendor": convert_pandas_types(row.get("vendor")),
            "category": convert_pandas_types(row.get("category")),
        },
        "cargo_description": {
            "main_description": convert_pandas_types(row.get("main_description_(po)")),
            "sub_description": convert_pandas_types(row.get("sub_description")),
        },
        "financial": {
            "incoterms": convert_pandas_types(row.get("incoterms")),
            "currency": convert_pandas_types(row.get("currency")),
            "invoice_value": convert_pandas_types(row.get("invoice_value__(a)")),
            "freight": convert_pandas_types(row.get("freight__(b)")),
            "insurance": convert_pandas_types(row.get("insurance__(c)")),
            "cif_value": convert_pandas_types(row.get("cif_value__(a+b+c)")),
        },
        "logistics": {
            "coe": convert_pandas_types(row.get("coe")),
            "pol": convert_pandas_types(row.get("pol")),
            "pod": convert_pandas_types(row.get("pod")),
            "bl_awb_no": convert_pandas_types(row.get("b/l_no./__awb_no.")),
            "vessel_name": convert_pandas_types(row.get("vessel_name/__flight_no.")),
            "vessel_imo_no": convert_pandas_types(row.get("vessel_imo_no.")),
            "shipping_line": convert_pandas_types(row.get("shipping_line")),
            "forwarder": convert_pandas_types(row.get("forwarder")),
            "ship_mode": convert_pandas_types(row.get("ship__mode")),
        },
        "containers": {
            "pkg": convert_pandas_types(row.get("pkg")),
            "20dc": convert_pandas_types(row.get("20dc")),
            "40dc": convert_pandas_types(row.get("40dc")),
            "40hq": convert_pandas_types(row.get("40hq")),
            "45hq": convert_pandas_types(row.get("45hq")),
            "20ot_in": convert_pandas_types(row.get("20ot(in)")),
            "20ot_oh": convert_pandas_types(row.get("20ot(oh)")),
            "40ot_in": convert_pandas_types(row.get("40ot(in)")),
            "40ot_oh": convert_pandas_types(row.get("40ot(oh)")),
            "20fr_in": convert_pandas_types(row.get("20fr(in)")),
            "40fr_in": convert_pandas_types(row.get("40fr(in)")),
            "20fr_fv": convert_pandas_types(row.get("20fr(fv)")),
            "40fr_ow": convert_pandas_types(row.get("40fr(ow)")),
            "20fr_ow_oh": convert_pandas_types(row.get("20fr(ow,oh)")),
            "40fr_ow_oh": convert_pandas_types(row.get("40fr(ow,oh)")),
            "40fr_ow_ol": convert_pandas_types(row.get("40fr(ow,ol)")),
            "lcl": convert_pandas_types(row.get("lcl")),
        },
        "quantities": {
            "qty_of_cntr": convert_pandas_types(row.get("qty_of_cntr")),
            "g_bulk": convert_pandas_types(row.get("g_bulk")),
            "o_bulk": convert_pandas_types(row.get("o_bulk")),
            "h_bulk": convert_pandas_types(row.get("h_bulk")),
            "gwt_kg": convert_pandas_types(row.get("gwt_(kg)")),
            "cbm": convert_pandas_types(row.get("cbm")),
            "r_t_grand_total": convert_pandas_types(row.get("r/t_(grand-_total)")),
            "a_cwt_kg": convert_pandas_types(row.get("a_cwt(kg)")),
        },
        "schedule": {
            "etd": convert_pandas_types(row.get("etd")),
            "atd": convert_pandas_types(row.get("atd")),
            "eta": convert_pandas_types(row.get("eta")),
            "ata": convert_pandas_types(row.get("ata")),
        },
        "customs": {
            "attestation_date": convert_pandas_types(row.get("attestation_date")),
            "do_collection": convert_pandas_types(row.get("do_collection")),
            "customs_start": convert_pandas_types(row.get("customs_start")),
            "customs_close": convert_pandas_types(row.get("customs_close")),
            "custom_code": convert_pandas_types(row.get("custom_code")),
            "duty_amt_aed": convert_pandas_types(row.get("duty_amt_(aed)")),
            "vat_amt_aed": convert_pandas_types(row.get("vat_amt_(aed)")),
        },
        "delivery_locations": {
            "shu": convert_pandas_types(row.get("shu")),
            "mir": convert_pandas_types(row.get("mir")),
            "das": convert_pandas_types(row.get("das")),
            "agi": convert_pandas_types(row.get("agi")),
            "dsv_indoor": convert_pandas_types(row.get("dsv_indoor")),
            "dsv_outdoor": convert_pandas_types(row.get("dsv_outdoor")),
            "dsv_mzd": convert_pandas_types(row.get("dsv_mzd")),
            "jdn_mzd": convert_pandas_types(row.get("jdn_mzd")),
            "jdn_waterfront": convert_pandas_types(row.get("jdn_waterfront")),
            "mosb": convert_pandas_types(row.get("mosb")),
            "aaa_storage": convert_pandas_types(row.get("aaa_storage")),
            "zener_wh": convert_pandas_types(row.get("zener_(wh)")),
            "hauler": convert_pandas_types(row.get("hauler")),
            "dg_storage": convert_pandas_types(row.get("dg_storage")),
            "vijay_tanks": convert_pandas_types(row.get("vijay_tanks")),
            "delivery_date": convert_pandas_types(row.get("delivery_date")),
        },
    }


def convert_excel_to_json():
    """Excel 파일을 JSON으로 변환"""

    # Excel 파일 읽기
    print("Excel 파일 읽기 시작...")
    df = pd.read_excel("HVDC STATUS(20250815).xlsx", sheet_name=0)
    print(f"Excel 파일 읽기 완료: {len(df)}개 행, {len(df.columns)}개 컬럼")

    # 컬럼명 정규화
    df.columns = [
        col.strip().replace("\n", " ").replace(" ", "_").lower() for col in df.columns
    ]

    # 출력 디렉토리 생성
    output_dir = Path("excel_output")
    output_dir.mkdir(exist_ok=True)

    # CSV 저장
    csv_file = output_dir / "HVDC_STATUS_converted.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8")
    print(f"CSV 파일 저장 완료: {csv_file}")

    # 전체 데이터를 구조화된 JSON으로 변환
    print("전체 데이터 JSON 변환 시작...")
    structured_shipments = []

    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"진행률: {idx}/{len(df)} ({idx/len(df)*100:.1f}%)")

        structured_shipment = structure_shipment_data(row)
        structured_shipments.append(structured_shipment)

    print(f"JSON 구조화 완료: {len(structured_shipments)}개 선적 데이터")

    # 전체 데이터 JSON 저장
    full_json_file = output_dir / "HVDC_STATUS_full.json"
    with open(full_json_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "metadata": {
                    "source_file": "HVDC STATUS(20250815).xlsx",
                    "total_records": len(df),
                    "generated_at": pd.Timestamp.now().isoformat(),
                    "schema_version": "1.0",
                    "description": "HVDC STATUS 전체 데이터 - HVDC CODE별 완전한 정보 구조화",
                },
                "shipments": structured_shipments,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"전체 JSON 파일 저장 완료: {full_json_file}")

    # 통계 정보
    print("\n=== 변환 통계 ===")
    print(f"총 레코드 수: {len(df)}")
    print(f"총 컬럼 수: {len(df.columns)}")
    print(f"구조화된 선적 데이터: {len(structured_shipments)}개")

    # 주요 컬럼 정보
    print("\n=== 주요 컬럼 완성도 ===")
    key_columns = [
        "hvdc_code",
        "vendor",
        "vessel_name/__flight_no.",
        "etd",
        "eta",
        "cif_value__(a+b+c)",
    ]
    for col in key_columns:
        if col in df.columns:
            non_null_count = df[col].notna().sum()
            print(f"{col}: {non_null_count}개 값 (총 {len(df)}개 중)")

    # 파일 크기 확인
    file_size = full_json_file.stat().st_size / (1024 * 1024)  # MB
    print(f"\n생성된 JSON 파일 크기: {file_size:.2f} MB")


if __name__ == "__main__":
    convert_excel_to_json()
