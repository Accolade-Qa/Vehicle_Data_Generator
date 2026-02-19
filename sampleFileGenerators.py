import csv
import os
import random
from datetime import datetime, timedelta

import pandas as pd

import data


def _ensure_output_dir(output_dir: str = "output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def generate_ota_sheet_csv(num_records: int = 10, output_dir: str = "output") -> str:
    output_dir = _ensure_output_dir(output_dir)
    output_file = os.path.join(output_dir, "Sample_OTA_Sheet.csv")

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IMEI"])
        for i in range(num_records):
            writer.writerow([data.get_record_by_index(i)["imei"]])

    return output_file


def generate_save_device_vin_csv(num_records: int = 10, output_dir: str = "output") -> str:
    output_dir = _ensure_output_dir(output_dir)
    output_file = os.path.join(output_dir, "Sample_Save_Device_Vin.csv")

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["imei", "vin"])
        for i in range(num_records):
            record = data.get_record_by_index(i)
            writer.writerow([record["imei"], record["vin"]])

    return output_file


def generate_save_device_state_csv(num_records: int = 10, output_dir: str = "output") -> str:
    output_dir = _ensure_output_dir(output_dir)
    output_file = os.path.join(output_dir, "Sample_Save_Device_State.csv")
    states = list(data.RTO_CODES.keys())

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["imei", "state"])
        for i in range(num_records):
            imei = data.get_record_by_index(i)["imei"]
            writer.writerow([imei, random.choice(states)])

    return output_file


def generate_dispatch_sheet_excel(num_records: int = 10, output_dir: str = "output") -> str:
    output_dir = _ensure_output_dir(output_dir)
    output_file = os.path.join(output_dir, "Sample_Dispatch_Sheet.xlsx")

    start_date = datetime.today() - timedelta(days=60)
    records = []
    for i in range(num_records):
        record = data.get_record_by_index(i)
        records.append({
            "SR_NO": i + 1,
            "TCU Model Name": "AEPL051400",
            "Prod.Date": (start_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "UIN": record["uin"],
            "IMEI": record["imei"],
            "ICCID": record["iccid"],
            "TML Part No.": f"5088547{i:06d}",
            "TCU FW": "5.2.3",
            "Bootstrap Exp": (datetime.today() + timedelta(days=365)).strftime("%d.%m.%Y"),
            "TCU Test Status": "OK",
            "Emission Type": "A4G",
            "SIM Operator ": random.choice(["BSNL", "Airtel", "Jio"]),
            "SIM Vendor": random.choice(["Sensorise", "Airtel", "Jio"]),
        })

    pd.DataFrame(records).to_excel(output_file, index=False)
    return output_file


def generate_all_sample_files(num_records: int = 10, output_dir: str = "output") -> dict:
    return {
        "ota_sheet": generate_ota_sheet_csv(num_records, output_dir),
        "save_device_vin": generate_save_device_vin_csv(num_records, output_dir),
        "save_device_state": generate_save_device_state_csv(num_records, output_dir),
        "dispatch_sheet": generate_dispatch_sheet_excel(num_records, output_dir),
    }
