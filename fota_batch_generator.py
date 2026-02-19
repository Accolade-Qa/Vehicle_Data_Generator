import csv
import os

import data
from dynamic_fields import DynamicFieldFactory
from settings import SETTINGS


def generate_fota_batch_csv(
    output_file: str = "fota_batch.csv",
    number_of_records: int = 5,
    ufw_version: str | None = None,
    model: str | None = None,
    output_dir: str | None = None,
):
    dataset = data.get_all_data()
    if number_of_records > len(dataset):
        raise ValueError(f"Requested {number_of_records} records, but only {len(dataset)} are available.")

    output_dir = output_dir or SETTINGS.default_output_dir
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)
    field_factory = DynamicFieldFactory(data.RTO_CODES)

    with open(output_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["UIN", "UFW", "MODEL", "STATE", "IMEI"])

        for index in range(number_of_records):
            record = dataset[index]
            writer.writerow([
                record["uin"],
                ufw_version or SETTINGS.default_fota_ufw,
                model or SETTINGS.default_fota_model,
                field_factory.random_state(),
                record["imei"],
            ])

    print(f"{number_of_records} FOTA records written to '{output_path}'")
    return output_path
