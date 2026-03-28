import csv
import os
from datetime import datetime, timedelta

import pandas as pd

from . import data
from .dynamic_fields import DynamicFieldFactory
from .settings import SETTINGS


def _ensure_output_dir(output_dir: str | None = None) -> str:
    resolved_dir = output_dir or SETTINGS.default_output_dir
    os.makedirs(resolved_dir, exist_ok=True)
    return resolved_dir


def generate_ota_sheet_csv(num_records: int = 10, output_dir: str | None = None) -> str:
    output_file = os.path.join(_ensure_output_dir(output_dir), "sample_ota_sheet.csv")
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IMEI"])
        for index in range(num_records):
            writer.writerow([data.get_record_by_index(index)["imei"]])
    return output_file


def generate_save_device_vin_csv(num_records: int = 10, output_dir: str | None = None) -> str:
    output_file = os.path.join(_ensure_output_dir(output_dir), "sample_save_device_vin.csv")
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["imei", "vin"])
        for index in range(num_records):
            record = data.get_record_by_index(index)
            writer.writerow([record["imei"], record["vin"]])
    return output_file


def generate_save_device_state_csv(num_records: int = 10, output_dir: str | None = None) -> str:
    output_file = os.path.join(_ensure_output_dir(output_dir), "sample_save_device_state.csv")
    field_factory = DynamicFieldFactory(data.RTO_CODES)
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["imei", "state"])
        for index in range(num_records):
            writer.writerow([data.get_record_by_index(index)["imei"], field_factory.random_state()])
    return output_file


def generate_dispatch_sheet_excel(num_records: int = 10, output_dir: str | None = None) -> str:
    output_file = os.path.join(_ensure_output_dir(output_dir), "sample_dispatch_sheet.xlsx")
    start_date = datetime.today() - timedelta(days=60)
    field_factory = DynamicFieldFactory(data.RTO_CODES)

    records = []
    for index in range(num_records):
        record = data.get_record_by_index(index)
        records.append({
            "SR_NO": index + 1,
            "TCU Model Name": SETTINGS.ticket_device_model,
            "Prod.Date": (start_date + timedelta(days=index)).strftime("%Y-%m-%d"),
            "UIN": record["uin"],
            "IMEI": record["imei"],
            "ICCID": record["iccid"],
            "TML Part No.": f"5088547{index:06d}",
            "TCU FW": "5.2.3",
            "Bootstrap Exp": (datetime.today() + timedelta(days=365)).strftime("%d.%m.%Y"),
            "TCU Test Status": "OK",
            "Emission Type": "A4G",
            "SIM Operator": field_factory.rng.choice(["BSNL", "Airtel", "Jio"]),
            "SIM Vendor": field_factory.rng.choice(["Sensorise", "Airtel", "Jio"]),
        })

    pd.DataFrame(records).to_excel(output_file, index=False)
    return output_file


def generate_all_sample_files(num_records: int = 10, output_dir: str | None = None) -> dict:
    return {
        "ota_sheet": generate_ota_sheet_csv(num_records, output_dir),
        "save_device_vin": generate_save_device_vin_csv(num_records, output_dir),
        "save_device_state": generate_save_device_state_csv(num_records, output_dir),
        "dispatch_sheet": generate_dispatch_sheet_excel(num_records, output_dir),
    }
