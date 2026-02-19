import csv
import os
import random

import data


def generate_fota_batch_csv(output_file, number_of_records, ufw_version=None, model=None):
    """
    Generate FOTA CSV with sample-compatible headers:
    UIN, UFW, MODEL, STATE, IMEI.
    """
    if not hasattr(data, "get_all_data"):
        raise AttributeError("data module must define get_all_data().")

    dataset = data.get_all_data()
    if number_of_records > len(dataset):
        raise ValueError(
            f"Requested {number_of_records} records, but only {len(dataset)} are available."
        )

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", output_file)

    with open(output_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["UIN", "UFW", "MODEL", "STATE", "IMEI"])

        for i in range(number_of_records):
            record = dataset[i]
            state = random.choice(list(data.RTO_CODES.keys()))

            writer.writerow([
                record["uin"],
                ufw_version or "5.2.8_TST03",
                model or "4G",
                state,
                record["imei"],
            ])

    print(f"{number_of_records} FOTA records written successfully to '{output_path}'")
    return output_path
