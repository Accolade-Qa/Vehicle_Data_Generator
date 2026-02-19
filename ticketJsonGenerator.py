# ---------------------------------------------------------
# ticketJsonGenerator.py — Ticketing Tool JSON Generator
# ---------------------------------------------------------
import json
import os
import random
from datetime import datetime
import data  # Unified dataset and RTO info

DEVICE_MODEL = "AEPL051400"
DEVICE_MAKE = "ACCOLADE"


def _pick_rto():
    """Select a random RTO code and corresponding state."""
    state = random.choice(list(data.RTO_CODES.keys()))
    rto_code = random.choice(data.RTO_CODES[state])
    return rto_code, state


def _generate_random_reg_number():
    """Generate a pseudo-random vehicle registration number."""
    state = random.choice(list(data.RTO_CODES.keys()))
    rto_code = random.choice(data.RTO_CODES[state])[:2]  # e.g., "MH"
    return f"{rto_code}{random.randint(10,99)}{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))}{random.randint(1000,9999)}"


def generate_json_data(num_records: int = 5, output_dir: str = "output"):
    """
    Generates ticketing tool JSON using deterministic dataset and random RTO data.
    Output file: output/ticketing_tool_data_<date>.json
    """
    dataset = data.get_all_data()
    vehicles = []

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_records):
        record = dataset[i % len(dataset)]
        rto_code, rto_state = _pick_rto()

        vehicle = {
            "VIN_NO": record["vin"],
            "ICCID": record["iccid"],
            "UIN_NO": record["uin"],
            "DEVICE_IMEI": record["imei"],
            "DEVICE_MAKE": DEVICE_MAKE,
            "DEVICE_MODEL": DEVICE_MODEL,
            "ENGINE_NO": f"ENGINE_SR_N_{random.randint(100000,999999)}",
            "REG_NUMBER": _generate_random_reg_number(),
            "REGISTERED_MOBILE_NUMBER": "7385862781",
            "VEHICLE_OWNER_FIRST_NAME": f"Owner_{i+1}",
            "VEHICLE_OWNER_LAST_NAME": "Lastname",
            "ADDRESS_LINE_1": "Sample Address Line 1",
            "ADDRESS_LINE_2": "Sample Address Line 2",
            "VEHICLE_OWNER_CITY": "City",
            "VEHICLE_OWNER_DISTRICT": "District",
            "VEHICLE_OWNER_STATE": rto_state,
            "VEHICLE_OWNER_COUNTRY": "India",
            "VEHICLE_OWNER_PINCODE": f"{random.randint(100000,999999)}",
            "VEHICLE_OWNER_REGISTERED_MOBILE": "7385862781",
            "POS_CODE": f"POS{random.randint(100,999)}",
            "POA_DOC_NAME": "POA_DOC",
            "POA_DOC_NO": f"POA{random.randint(1000,9999)}",
            "POI_DOC_TYPE": "AADHAR",
            "POI_DOC_NO": f"ADHAR{random.randint(1000,9999)}",
            "RTO_OFFICE_CODE": rto_code,
            "RTO_STATE": rto_state,
            "PRIMARY_OPERATOR": "AIRTEL",
            "SECONDARY_OPERATOR": "BSNL",
            "PRIMARY_MOBILE_NUMBER": "8765284847",
            "SECONDARY_MOBILE_NUMBER": "7992635726",
            "VEHICLE_MODEL": "Bugatti",
            "DEALER_CODE": f"{random.randint(1000,9999)}",
            "COMMERCIAL_ACTIVATION_START_DATE": "2024-10-04",
            "COMMERCIAL_ACTIVATION_EXPIRY_DATE": "2027-10-05",
            "MFG_YEAR": "2024",
            "ACCOLADE_POSTING_DATE_TIME": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "INVOICE_DATE": "2024-10-04",
            "INVOICE_NUMBER": f"AEPL{random.randint(100000,999999)}",
            "CERTIFICATE_VALIDITY_DURATION_IN_YEAR": 2
        }

        vehicles.append(vehicle)

    date_str = datetime.today().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"ticketing_tool_data_{date_str}.json")

    with open(output_file, "w") as f:
        json.dump(vehicles, f, indent=4)

    print(f"✅ {num_records} ticketing records saved to '{output_file}'")
    return output_file