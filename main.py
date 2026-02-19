from fotaBatchGenerator import generate_fota_batch_csv
from crmApiGenerator import send_ticket_generation_requests
from instititionalSalesGenerator import generate_institutional_sales
from sampleFileGenerators import generate_all_sample_files
from simBatchGenerator import generate_sim_batch_csv
from ticketDataCsvGenerator import generate_ticket_data_csv
from ticketJsonGenerator import generate_json_data


def get_int_input(prompt, default):
    try:
        value = input(prompt).strip()
        return int(value) if value else default
    except ValueError:
        print(f"Invalid input. Using default value: {default}")
        return default


def main():
    print("\n--- Vehicle Data Generator ---")
    print("1. Generate SIM Batch Details")
    print("2. Generate Ticketing Tool JSON Data")
    print("3. Generate FOTA Batch CSV File")
    print("4. Generate Institutional Sales Data")
    print("5. Generate Additional Sample Files")
    print("6. Generate Ticket Data CSV")
    print("7. Send CRM Ticket API Requests")
    print("----------------------------------------------------")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        number_of_records = get_int_input("Enter number of records (default: 5): ", 5)
        generate_sim_batch_csv(number_of_records)
    elif choice == "2":
        number_of_records = get_int_input("Enter number of records (default: 2): ", 2)
        generate_json_data(number_of_records)
    elif choice == "3":
        output_file = input("Enter output file name (default: fota_batch.csv): ").strip() or "fota_batch.csv"
        record_count = get_int_input("Enter number of records (default: 5): ", 5)
        ufw_version = input("Enter firmware version (default: 5.2.8_TST03): ").strip() or "5.2.8_TST03"
        model = input("Enter device model (default: 4G): ").strip() or "4G"
        generate_fota_batch_csv(output_file, record_count, ufw_version, model)
    elif choice == "4":
        number_of_records = get_int_input("Enter number of records (default: 5): ", 5)
        output_dir = input("Enter output directory (leave blank for current): ").strip() or None
        generate_institutional_sales(number_of_records, output_dir)
    elif choice == "5":
        number_of_records = get_int_input("Enter number of records (default: 5): ", 5)
        output_dir = input("Enter output directory (default: output): ").strip() or "output"
        generated = generate_all_sample_files(number_of_records, output_dir)
        print("\nGenerated files:")
        for key, path in generated.items():
            print(f"- {key}: {path}")
    elif choice == "6":
        number_of_records = get_int_input("Enter number of records (default: 10): ", 10)
        output_file = input("Enter output file name (default: generated_records.csv): ").strip() or "generated_records.csv"
        output_dir = input("Enter output directory (default: output): ").strip() or "output"
        generate_ticket_data_csv(number_of_records, output_file, output_dir)
    elif choice == "7":
        vin_start = get_int_input("Enter VIN start number (default: 40): ", 40)
        vin_end = get_int_input("Enter VIN end number (default: 45): ", 45)
        vin_prefix = input("Enter VIN prefix (default: SURAJ07082025_): ").strip() or "SURAJ07082025_"
        send_ticket_generation_requests(vin_start=vin_start, vin_end=vin_end, vin_prefix=vin_prefix)
    else:
        print("\nInvalid choice. Please select a valid option.")


if __name__ == "__main__":
    try:
        main()
        print("\nTask completed successfully.")
    except Exception as error:
        print(f"\nAn error occurred: {error}")
