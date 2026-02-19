import json
import os
from datetime import datetime

from . import data
from .dynamic_fields import DynamicFieldFactory
from .settings import SETTINGS


def generate_ticket_json(num_records: int = 5, output_dir: str | None = None):
    output_dir = output_dir or SETTINGS.default_output_dir
    os.makedirs(output_dir, exist_ok=True)

    field_factory = DynamicFieldFactory(data.RTO_CODES)
    vehicles = []
    dataset = data.get_all_data()

    for index in range(num_records):
        record = dataset[index % len(dataset)]
        rto_state, rto_code = field_factory.random_rto()

        vehicles.append({
            "VIN_NO": record["vin"],
            "ICCID": record["iccid"],
            "UIN_NO": record["uin"],
            "DEVICE_IMEI": record["imei"],
            "DEVICE_MAKE": SETTINGS.device_make,
            "DEVICE_MODEL": SETTINGS.ticket_device_model,
            "ENGINE_NO": f"ENGINE_SR_N_{field_factory.rng.randint(100000, 999999)}",
            "REG_NUMBER": field_factory.random_registration_number(),
            "REGISTERED_MOBILE_NUMBER": field_factory.random_mobile(),
            "VEHICLE_OWNER_FIRST_NAME": f"Owner_{index + 1}",
            "VEHICLE_OWNER_LAST_NAME": "Lastname",
            "ADDRESS_LINE_1": "Sample Address Line 1",
            "ADDRESS_LINE_2": "Sample Address Line 2",
            "VEHICLE_OWNER_CITY": "City",
            "VEHICLE_OWNER_DISTRICT": "District",
            "VEHICLE_OWNER_STATE": rto_state,
            "VEHICLE_OWNER_COUNTRY": "India",
            "VEHICLE_OWNER_PINCODE": field_factory.random_pincode(),
            "VEHICLE_OWNER_REGISTERED_MOBILE": field_factory.random_mobile(),
            "POS_CODE": f"POS{field_factory.rng.randint(100, 999)}",
            "POA_DOC_NAME": "POA_DOC",
            "POA_DOC_NO": f"POA{field_factory.rng.randint(1000, 9999)}",
            "POI_DOC_TYPE": "AADHAR",
            "POI_DOC_NO": f"ADHAR{field_factory.rng.randint(1000, 9999)}",
            "RTO_OFFICE_CODE": rto_code,
            "RTO_STATE": rto_code[:2],
            "PRIMARY_OPERATOR": "AIRTEL",
            "SECONDARY_OPERATOR": "BSNL",
            "PRIMARY_MOBILE_NUMBER": field_factory.random_mobile(),
            "SECONDARY_MOBILE_NUMBER": field_factory.random_mobile(),
            "VEHICLE_MODEL": "Bugatti",
            "DEALER_CODE": f"{field_factory.rng.randint(1000, 9999)}",
            "COMMERCIAL_ACTIVATION_START_DATE": "2024-10-04",
            "COMMERCIAL_ACTIVATION_EXPIRY_DATE": "2027-10-05",
            "MFG_YEAR": "2024",
            "ACCOLADE_POSTING_DATE_TIME": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "INVOICE_DATE": "2024-10-04",
            "INVOICE_NUMBER": f"AEPL{field_factory.rng.randint(100000, 999999)}",
            "CERTIFICATE_VALIDITY_DURATION_IN_YEAR": 2,
        })

    output_file = os.path.join(output_dir, f"ticketing_tool_data_{datetime.today().strftime('%Y%m%d')}.json")
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(vehicles, file, indent=4)

    print(f"{num_records} ticketing records saved to '{output_file}'")
    return output_file
