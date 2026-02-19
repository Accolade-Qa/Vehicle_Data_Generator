# ---------------------------------------------------------
# institutionalSalesGenerator.py — Institutional Sales Data Generator
# ---------------------------------------------------------
import pandas as pd
from datetime import datetime, timedelta
import os
from data import (
    get_next_record,
    reset_pointer,
    RTO_CODES,
)

# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------
DEVICE_MODEL = "AEPL051400"  # single model (no 2G)
DEVICE_MAKE = "Accolade"

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
    "SECONDARY": ["BHA", "Vodafone"]
}

VEHICLE_MODELS = ["NANO", "Sedan", "SUV", "Electric", "Truck"]

# ---------------------------------------------------------
# MAIN GENERATOR FUNCTION
# ---------------------------------------------------------
def generate_institutional_sales(number_of_records=10, output_dir=None):
    """
    Generate an Institutional Sales Excel file using sequential constant dataset values.
    Output is always saved inside the 'output' directory.
    """
    reset_pointer()  # reset the data pointer

    base_vin_prefix = "SURAJ30072025"
    start_date = datetime.today()
    expiry_date = start_date + timedelta(days=730)

    # Ensure output folder exists
    output_dir = output_dir or os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Flatten RTO state-code pairs
    rto_pairs = [(state, code) for state, codes in RTO_CODES.items() for code in codes]

    records = []
    for i in range(number_of_records):
        base_record = get_next_record()
        uin = base_record["uin"]
        iccid = base_record["iccid"]
        imei = base_record["imei"]
        vin = base_record["vin"]

        # Rotate through RTO state and code list
        _, rto_code = rto_pairs[i % len(rto_pairs)]
        rto_state = rto_code[:2]
        primary_operator = OPERATORS["PRIMARY"][i % len(OPERATORS["PRIMARY"])]
        secondary_operator = OPERATORS["SECONDARY"][i % len(OPERATORS["SECONDARY"])]
        vehicle_model = VEHICLE_MODELS[i % len(VEHICLE_MODELS)]

        record = {
            "VIN_NO": vin,
            "ICCID": iccid,
            "UIN_NO": uin,
            "DEVICE_IMEI": imei,
            "DEVICE_MAKE": DEVICE_MAKE,
            "DEVICE_MODEL": DEVICE_MODEL,
            "ENGINE_NO": f"ENGINE_FIXED_{i+1:05d}",
            "REG_NUMBER": f"{rto_code}AB{i+1000}",
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
            "VEHICLE_OWNER_REGISTERED_MOBILE": 9999999999 - i,
            "POS_CODE": FIXED_DOCS["POS_CODE"],
            "POA_DOC_NAME": FIXED_DOCS["POA_DOC_NAME"],
            "POA_DOC_NO": FIXED_DOCS["POA_DOC_NO"],
            "POI_DOC_TYPE": FIXED_DOCS["POI_DOC_TYPE"],
            "POI_DOC_NO": FIXED_DOCS["POI_DOC_NO"],
            "RTO_OFFICE_CODE": rto_code,
            "RTO_STATE": rto_state,
            "PRIMARY_OPERATOR": primary_operator,
            "SECONDARY_OPERATOR": secondary_operator,
            "PRIMARY_MOBILE_NUMBER": 8888888888 - i,
            "SECONDARY_MOBILE_NUMBER": 7777777777 - i,
            "VEHICLE_MODEL": vehicle_model,
            "DEALER_CODE": 1000 + i,
            "COMMERCIAL_ACTIVATION_START_DATE": start_date.strftime('%Y-%m-%d'),
            "COMMERCIAL_ACTIVATION_EXPIRY_DATE": expiry_date.strftime('%Y-%m-%d'),
            "MFG_YEAR": 2024,
            "ACCOLADE_POSTING_DATE_TIME": start_date.strftime('%Y-%m-%d'),
            "INVOICE_DATE": start_date.strftime('%Y-%m-%d'),
            "INVOICE_NUMBER": f"AEPL{100000000 + i}",
            "CERTIFICATE_VALIDITY_DURATION_IN_YEAR": 3
        }

        records.append(record)

    df = pd.DataFrame(records)
    file_name = f"Institutional_Sales_{datetime.today().strftime('%Y%m%d')}.xlsx"
    output_path = os.path.join(output_dir, file_name)
    df.to_excel(output_path, index=False)

    print(f"✅ Institutional Sales file generated successfully: {output_path}")
    return df
