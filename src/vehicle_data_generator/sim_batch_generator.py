import csv
import os
from datetime import datetime

from . import data
from .dynamic_fields import DynamicFieldFactory
from .settings import SETTINGS

SIM_STATUS_OPTIONS = ["Active", "Inactive"]
ACTIVATION_STATUS_OPTIONS = ["Pending", "Completed"]
VAHAN_UPLOAD_STATUS_OPTIONS = ["Pending", "Completed", "Ongoing"]

PRIMARY_OPERATORS = ["Jio", "Airtel", "Vodafone", "BSNL", "Idea"]
SECONDARY_OPERATORS = ["Vodafone", "Airtel", "Jio", "BSNL", "MTNL"]

VEHICLE_MODELS = [
    "HYUNDAI Hatchback",
    "TOYOTA Sedan",
    "SUZUKI SUV",
    "BMW Hatchback",
    "TATA Commercial",
    "HONDA Hybrid",
    "KIA SUV",
    "MAHINDRA Pickup",
    "RENAULT MPV",
    "NISSAN Crossover",
]


def generate_sim_batch_csv(num_records: int = 10, output_dir: str | None = None):
    field_factory = DynamicFieldFactory(data.RTO_CODES)
    output_dir = output_dir or SETTINGS.default_output_dir
    os.makedirs(output_dir, exist_ok=True)

    date_str = datetime.today().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"card_details_{date_str}.csv")

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "CHASSIS_NO", "ICCID", "IMEI", "SERIAL_NO",
            "DEVICE_MAKE", "DEVICE_MODEL", "ENGINE_NO",
            "REG_NUMBER", "DEALER_NAME", "DEALER_CODE",
            "RTO_OFFICE_CODE", "RTO_STATE",
            "PRIMARY_OPERATOR", "PRIMARY_MOBILE_NUMBER",
            "SECONDARY_OPERATOR", "SECONDARY_MOBILE_NUMBER",
            "VEHICLE_MODEL", "SIM_STATUS",
            "ACTIVATION_STATUS", "ACTIVATION_STATUS_DATE",
            "ACTIVATION_EXPIRY", "VAHAN_UPLOAD_STATUS",
        ])

        for i in range(num_records):
            record = data.get_record_by_index(i)
            rto_state, rto_office_code = field_factory.random_rto()

            activation_date = datetime.today().strftime("%d-%b-%y")
            activation_expiry = (datetime.today() + timedelta(days=365 * 5)).strftime("%d-%b-%y")

            writer.writerow([
                record["vin"],
                record["iccid"],
                record["imei"],
                record["uin"],
                SETTINGS.device_make,
                SETTINGS.device_model_4g,
                f"ENG{i:05d}",
                field_factory.random_registration_number(),
                f"Dealer_{rto_state[:3].upper()}",
                f"100{i:04d}",
                rto_office_code,
                rto_state,
                field_factory.rng.choice(PRIMARY_OPERATORS),
                field_factory.random_mobile(),
                field_factory.rng.choice(SECONDARY_OPERATORS),
                field_factory.random_mobile(),
                field_factory.rng.choice(VEHICLE_MODELS),
                field_factory.rng.choice(SIM_STATUS_OPTIONS),
                field_factory.rng.choice(ACTIVATION_STATUS_OPTIONS),
                activation_date,
                activation_expiry,
                field_factory.rng.choice(VAHAN_UPLOAD_STATUS_OPTIONS),
            ])

    print(f"SIM batch with {num_records} records written to: {output_file}")
    return output_file
