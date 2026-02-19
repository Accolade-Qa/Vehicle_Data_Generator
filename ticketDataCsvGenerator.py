import csv
import os
import random
from datetime import datetime, timedelta


def _generate_random_imei():
    return "".join(str(random.randint(0, 9)) for _ in range(15))


def _generate_random_iccid():
    return "8991" + "".join(str(random.randint(0, 9)) for _ in range(16))


def _generate_random_vin():
    return "ACCDEV" + "".join(str(random.randint(0, 9)) for _ in range(9))


def _generate_random_uin():
    return "ACON4NA2024" + "".join(str(random.randint(0, 9)) for _ in range(6))


def _generate_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%m/%d/%Y")


def generate_ticket_data_csv(number_of_records=10, output_file="generated_records.csv", output_dir="output"):
    """
    Generates ticket CSV in the same schema as the root script:
    uin, vinNo, iccid, imei, cardStatus, deviceModel, bootstrapExpiryDate,
    dealerState, vehicleModel, vehicleDispatchDate
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    card_status = "Active"
    dealer_state = "Maharashtra"
    device_model = "AEPL051400"
    vehicle_model = "COMM"

    current_year = datetime.now().year
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
                _generate_random_uin(),
                _generate_random_vin(),
                _generate_random_iccid(),
                _generate_random_imei(),
                card_status,
                device_model,
                _generate_random_date(bootstrap_start_date, bootstrap_end_date),
                dealer_state,
                vehicle_model,
                _generate_random_date(dispatch_start_date, dispatch_end_date),
            ])

    print(f"{number_of_records} records have been written to {output_path}.")
    return output_path
