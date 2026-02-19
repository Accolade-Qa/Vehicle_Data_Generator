import csv
import os
from datetime import datetime

from .dynamic_fields import DynamicFieldFactory
from .settings import SETTINGS
from . import data


def _random_uin(field_factory: DynamicFieldFactory):
    return "ACON4NA2024" + "".join(str(field_factory.rng.randint(0, 9)) for _ in range(6))


def _random_vin(field_factory: DynamicFieldFactory):
    return "ACCDEV" + "".join(str(field_factory.rng.randint(0, 9)) for _ in range(9))


def _random_iccid(field_factory: DynamicFieldFactory):
    return "8991" + "".join(str(field_factory.rng.randint(0, 9)) for _ in range(16))


def _random_imei(field_factory: DynamicFieldFactory):
    return "".join(str(field_factory.rng.randint(0, 9)) for _ in range(15))


def generate_ticket_data_csv(
    number_of_records: int = 10,
    output_file: str = "generated_records.csv",
    output_dir: str | None = None,
):
    output_dir = output_dir or SETTINGS.default_output_dir
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    current_year = datetime.now().year
    field_factory = DynamicFieldFactory(data.RTO_CODES)
    bootstrap_start_date = datetime(current_year, 1, 1)
    bootstrap_end_date = datetime(current_year + 5, 12, 31)
    dispatch_start_date = datetime(current_year, 1, 1)
    dispatch_end_date = datetime(current_year + 1, 12, 31)

    with open(output_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "uin",
            "vinNo",
            "iccid",
            "imei",
            "cardStatus",
            "deviceModel",
            "bootstrapExpiryDate",
            "dealerState",
            "vehicleModel",
            "vehicleDispatchDate",
        ])

        for _ in range(number_of_records):
            writer.writerow([
                _random_uin(field_factory),
                _random_vin(field_factory),
                _random_iccid(field_factory),
                _random_imei(field_factory),
                "Active",
                SETTINGS.ticket_device_model,
                field_factory.random_date(bootstrap_start_date, bootstrap_end_date, "%m/%d/%Y"),
                "Maharashtra",
                "COMM",
                field_factory.random_date(dispatch_start_date, dispatch_end_date, "%m/%d/%Y"),
            ])

    print(f"{number_of_records} records written to {output_path}")
    return output_path
