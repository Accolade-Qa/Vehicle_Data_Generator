import os
from datetime import datetime, timedelta

import pandas as pd

from . import data
from .dynamic_fields import DynamicFieldFactory
from .settings import SETTINGS

VEHICLE_OWNER = {
    "FIRST_NAME": "SBSB",
    "MIDDLE_NAME": "S",
    "LAST_NAME": "BHALERAO",
    "ADDRESS_LINE_1": "SHIVANE",
    "ADDRESS_LINE_2": "SHIVANE",
    "CITY": "PUNE",
    "DISTRICT": "PUNE",
    "STATE": "MAHARASHTRA",
    "COUNTRY": "INDIA",
    "PINCODE": 411045,
}

FIXED_DOCS = {
    "POS_CODE": "AB123",
    "POA_DOC_NAME": "PANAB123",
    "POA_DOC_NO": "PAN1AB123",
    "POI_DOC_TYPE": "ADHARAB123",
    "POI_DOC_NO": "ADHARXYZ123",
}

OPERATORS = {
    "PRIMARY": ["BSNL", "Airtel", "Jio"],
    "SECONDARY": ["BHA", "Vodafone"],
}

VEHICLE_MODELS = ["NANO", "Sedan", "SUV", "Electric", "Truck"]


def generate_institutional_sales(number_of_records: int = 10, output_dir: str | None = None):
    field_factory = DynamicFieldFactory(data.RTO_CODES)
    start_date = datetime.today()
    expiry_date = start_date + timedelta(days=730)
    output_dir = output_dir or SETTINGS.default_output_dir
    os.makedirs(output_dir, exist_ok=True)

    rto_pairs = [(state, code) for state, codes in data.RTO_CODES.items() for code in codes]
    records = []

    for index in range(number_of_records):
        base_record = data.get_record_by_index(index)
        _, rto_code = rto_pairs[index % len(rto_pairs)]

        records.append({
            "VIN_NO": base_record["vin"],
            "ICCID": base_record["iccid"],
            "UIN_NO": base_record["uin"],
            "DEVICE_IMEI": base_record["imei"],
            "DEVICE_MAKE": SETTINGS.device_make.title(),
            "DEVICE_MODEL": SETTINGS.ticket_device_model,
            "ENGINE_NO": f"ENGINE_FIXED_{index + 1:05d}",
            "REG_NUMBER": f"{rto_code}AB{index + 1000}",
            "VEHICLE_OWNER_FIRST_NAME": VEHICLE_OWNER["FIRST_NAME"],
            "VEHICLE_OWNER_MIDDLE_NAME": VEHICLE_OWNER["MIDDLE_NAME"],
            "VEHICLE_OWNER_LAST_NAME": VEHICLE_OWNER["LAST_NAME"],
            "ADDRESS_LINE_1": VEHICLE_OWNER["ADDRESS_LINE_1"],
            "ADDRESS_LINE_2": VEHICLE_OWNER["ADDRESS_LINE_2"],
            "VEHICLE_OWNER_CITY": VEHICLE_OWNER["CITY"],
            "VEHICLE_OWNER_DISTRICT": VEHICLE_OWNER["DISTRICT"],
            "VEHICLE_OWNER_STATE": VEHICLE_OWNER["STATE"],
            "VEHICLE_OWNER_COUNTRY": VEHICLE_OWNER["COUNTRY"],
            "VEHICLE_OWNER_PINCODE": VEHICLE_OWNER["PINCODE"],
            "VEHICLE_OWNER_REGISTERED_MOBILE": field_factory.random_mobile(),
            "POS_CODE": FIXED_DOCS["POS_CODE"],
            "POA_DOC_NAME": FIXED_DOCS["POA_DOC_NAME"],
            "POA_DOC_NO": FIXED_DOCS["POA_DOC_NO"],
            "POI_DOC_TYPE": FIXED_DOCS["POI_DOC_TYPE"],
            "POI_DOC_NO": FIXED_DOCS["POI_DOC_NO"],
            "RTO_OFFICE_CODE": rto_code,
            "RTO_STATE": rto_code[:2],
            "PRIMARY_OPERATOR": OPERATORS["PRIMARY"][index % len(OPERATORS["PRIMARY"])],
            "SECONDARY_OPERATOR": OPERATORS["SECONDARY"][index % len(OPERATORS["SECONDARY"])],
            "PRIMARY_MOBILE_NUMBER": field_factory.random_mobile(),
            "SECONDARY_MOBILE_NUMBER": field_factory.random_mobile(),
            "VEHICLE_MODEL": VEHICLE_MODELS[index % len(VEHICLE_MODELS)],
            "DEALER_CODE": 1000 + index,
            "COMMERCIAL_ACTIVATION_START_DATE": start_date.strftime("%Y-%m-%d"),
            "COMMERCIAL_ACTIVATION_EXPIRY_DATE": expiry_date.strftime("%Y-%m-%d"),
            "MFG_YEAR": 2024,
            "ACCOLADE_POSTING_DATE_TIME": start_date.strftime("%Y-%m-%d"),
            "INVOICE_DATE": start_date.strftime("%Y-%m-%d"),
            "INVOICE_NUMBER": f"AEPL{100000000 + index}",
            "CERTIFICATE_VALIDITY_DURATION_IN_YEAR": 3,
        })

    data_frame = pd.DataFrame(records)
    output_path = os.path.join(output_dir, f"institutional_sales_{datetime.today().strftime('%Y%m%d')}.xlsx")
    data_frame.to_excel(output_path, index=False)
    print(f"Institutional Sales file generated: {output_path}")
    return output_path
