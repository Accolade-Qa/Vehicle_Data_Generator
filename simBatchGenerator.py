# ---------------------------------------------------------
# simBatchGenerator.py — VAHAN-format SIM Batch CSV Generator (Dynamic Version)
# ---------------------------------------------------------
import csv
import os
import random
from datetime import datetime
import data

# Static fields
DEVICE_MAKE = "ACCOLADE"
DEVICE_MODEL = "ACON4NA"

# Dynamic options
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
    "NISSAN Crossover"
]


def get_random_rto():
    """Return a random (state, RTO code) tuple from data.RTO_CODES."""
    state = random.choice(list(data.RTO_CODES.keys()))
    rto_code = random.choice(data.RTO_CODES[state])
    return state, rto_code


def generate_sim_batch_csv(num_records: int = 10, output_dir: str = "output"):
    """
    Generates a VAHAN-format SIM batch CSV using data from data.py.
    Headers follow VAHAN upload structure.
    """
    dataset = data.get_all_data()
    os.makedirs(output_dir, exist_ok=True)

    date_str = datetime.today().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"Card_details_{date_str}.csv")

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
            "ACTIVATION_EXPIRY", "VAHAN_UPLOAD_STATUS"
        ])

        for i in range(num_records):
            record = data.get_record_by_index(i)
            rto_state, rto_office_code = get_random_rto()

            # Random dynamic fields
            primary_op = random.choice(PRIMARY_OPERATORS)
            secondary_op = random.choice(SECONDARY_OPERATORS)
            vehicle_model = random.choice(VEHICLE_MODELS)
            sim_status = random.choice(SIM_STATUS_OPTIONS)
            activation_status = random.choice(ACTIVATION_STATUS_OPTIONS)
            vahan_status = random.choice(VAHAN_UPLOAD_STATUS_OPTIONS)

            activation_date = datetime.today().strftime("%d-%b-%y")
            activation_expiry = (
                datetime.today().replace(year=datetime.today().year + 5)
            ).strftime("%d-%b-%y")

            # Write row
            writer.writerow([
                record["vin"],                       # CHASSIS_NO
                record["iccid"],                     # ICCID
                record["imei"],                      # IMEI
                record["uin"],                       # SERIAL_NO
                DEVICE_MAKE,
                DEVICE_MODEL,
                f"ENG{i:05d}",                      # ENGINE_NO
                f"REG{i:04d}",                      # REG_NUMBER
                f"Dealer_{rto_state[:3].upper()}",   # DEALER_NAME
                f"100{i:04d}",                      # DEALER_CODE
                rto_office_code,                     # RTO_OFFICE_CODE
                rto_state,                           # RTO_STATE
                primary_op,                          # PRIMARY_OPERATOR
                f"9{random.randint(100000000, 999999999)}",  # PRIMARY_MOBILE_NUMBER
                secondary_op,                        # SECONDARY_OPERATOR
                f"9{random.randint(100000000, 999999999)}",  # SECONDARY_MOBILE_NUMBER
                vehicle_model,                       # VEHICLE_MODEL
                sim_status,                          # SIM_STATUS
                activation_status,                   # ACTIVATION_STATUS
                activation_date,                     # ACTIVATION_STATUS_DATE
                activation_expiry,                   # ACTIVATION_EXPIRY
                vahan_status                         # VAHAN_UPLOAD_STATUS
            ])

    print(f"✅ VAHAN-format SIM batch with {num_records} records written to: {output_file}")
    return output_file