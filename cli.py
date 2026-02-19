import argparse

from crm_api_generator import send_ticket_generation_requests
from fota_batch_generator import generate_fota_batch_csv
from institutional_sales_generator import generate_institutional_sales
from sample_file_generators import generate_all_sample_files
from sim_batch_generator import generate_sim_batch_csv
from ticket_data_csv_generator import generate_ticket_data_csv
from ticket_json_generator import generate_ticket_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vehicle-data-generator", description="Vehicle data generation CLI tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sim_parser = subparsers.add_parser("sim-batch", help="Generate SIM batch CSV")
    sim_parser.add_argument("--records", type=int, default=10)
    sim_parser.add_argument("--output-dir", default=None)

    ticket_json_parser = subparsers.add_parser("ticket-json", help="Generate ticketing JSON")
    ticket_json_parser.add_argument("--records", type=int, default=5)
    ticket_json_parser.add_argument("--output-dir", default=None)

    fota_parser = subparsers.add_parser("fota-batch", help="Generate FOTA CSV")
    fota_parser.add_argument("--records", type=int, default=5)
    fota_parser.add_argument("--output-file", default="fota_batch.csv")
    fota_parser.add_argument("--ufw", default=None)
    fota_parser.add_argument("--model", default=None)
    fota_parser.add_argument("--output-dir", default=None)

    sales_parser = subparsers.add_parser("institutional-sales", help="Generate institutional sales XLSX")
    sales_parser.add_argument("--records", type=int, default=10)
    sales_parser.add_argument("--output-dir", default=None)

    samples_parser = subparsers.add_parser("sample-files", help="Generate sample format files")
    samples_parser.add_argument("--records", type=int, default=10)
    samples_parser.add_argument("--output-dir", default=None)

    ticket_csv_parser = subparsers.add_parser("ticket-csv", help="Generate ticket CSV")
    ticket_csv_parser.add_argument("--records", type=int, default=10)
    ticket_csv_parser.add_argument("--output-file", default="generated_records.csv")
    ticket_csv_parser.add_argument("--output-dir", default=None)

    api_parser = subparsers.add_parser("crm-api", help="Send CRM ticket API requests")
    api_parser.add_argument("--vin-start", type=int, default=40)
    api_parser.add_argument("--vin-end", type=int, default=45)
    api_parser.add_argument("--vin-prefix", default="SURAJ07082025_")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "sim-batch":
        generate_sim_batch_csv(num_records=args.records, output_dir=args.output_dir)
    elif args.command == "ticket-json":
        generate_ticket_json(num_records=args.records, output_dir=args.output_dir)
    elif args.command == "fota-batch":
        generate_fota_batch_csv(
            output_file=args.output_file,
            number_of_records=args.records,
            ufw_version=args.ufw,
            model=args.model,
            output_dir=args.output_dir,
        )
    elif args.command == "institutional-sales":
        generate_institutional_sales(number_of_records=args.records, output_dir=args.output_dir)
    elif args.command == "sample-files":
        generated_files = generate_all_sample_files(num_records=args.records, output_dir=args.output_dir)
        for key, value in generated_files.items():
            print(f"{key}: {value}")
    elif args.command == "ticket-csv":
        generate_ticket_data_csv(
            number_of_records=args.records,
            output_file=args.output_file,
            output_dir=args.output_dir,
        )
    elif args.command == "crm-api":
        send_ticket_generation_requests(
            vin_start=args.vin_start,
            vin_end=args.vin_end,
            vin_prefix=args.vin_prefix,
        )
    else:
        parser.print_help()
        return 1

    return 0
