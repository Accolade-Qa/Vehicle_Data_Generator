import argparse

from .crm_api_generator import send_ticket_generation_requests
from .fota_batch_generator import generate_fota_batch_csv
from .institutional_sales_generator import generate_institutional_sales
from .sample_file_generators import generate_all_sample_files
from .sim_batch_generator import generate_sim_batch_csv
from .ticket_data_csv_generator import generate_ticket_data_csv
from .ticket_json_generator import generate_ticket_json


class VDGHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    """Include defaults and preserve line breaks for richer CLI help text."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vdg",
        formatter_class=VDGHelpFormatter,
        description=(
            "VDG: Vehicle Data Generator CLI\n"
            "Generate CSV/JSON/XLSX artifacts and call CRM ticket APIs."
        ),
        epilog=(
            "Examples:\n"
            "  vdg sim-batch -r 20 -o output\n"
            "  vdg ticket-json -r 5 -o output\n"
            "  vdg fota-batch -r 10 -f fota.csv -u 5.2.9 -m 4G -o output\n"
            "  vdg crm-api -s 40 -e 45 -p VDGVIN_"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    sim_parser = subparsers.add_parser(
        "sim-batch",
        formatter_class=VDGHelpFormatter,
        help="Generate SIM batch CSV",
        description="Generate SIM batch CSV file with telematics and activation fields.",
    )
    sim_parser.add_argument("-r", type=int, default=10, help="Number of records to generate.")
    sim_parser.add_argument("-o", default=None, help="Output directory path for generated CSV.")

    ticket_json_parser = subparsers.add_parser(
        "ticket-json",
        formatter_class=VDGHelpFormatter,
        help="Generate ticketing JSON",
        description="Generate CRM ticket payload JSON records.",
    )
    ticket_json_parser.add_argument("-r", type=int, default=5, help="Number of JSON records to generate.")
    ticket_json_parser.add_argument("-o", default=None, help="Output directory path for generated JSON.")

    fota_parser = subparsers.add_parser(
        "fota-batch",
        formatter_class=VDGHelpFormatter,
        help="Generate FOTA CSV",
        description="Generate firmware-over-the-air batch CSV records.",
    )
    fota_parser.add_argument("-r", type=int, default=5, help="Number of FOTA records to generate.")
    fota_parser.add_argument("-f", default="fota_batch.csv", help="Output CSV filename.")
    fota_parser.add_argument("-u", default=None, help="UFW version override value.")
    fota_parser.add_argument("-m", default=None, help="Device model override value.")
    fota_parser.add_argument("-o", default=None, help="Output directory path for generated CSV.")

    sales_parser = subparsers.add_parser(
        "institutional-sales",
        formatter_class=VDGHelpFormatter,
        help="Generate institutional sales XLSX",
        description="Generate institutional sales Excel file with fixed and dynamic fields.",
    )
    sales_parser.add_argument("-r", type=int, default=10, help="Number of XLSX rows to generate.")
    sales_parser.add_argument("-o", default=None, help="Output directory path for generated XLSX.")

    samples_parser = subparsers.add_parser(
        "sample-files",
        formatter_class=VDGHelpFormatter,
        help="Generate sample format files",
        description="Generate all sample files (OTA, VIN map, state map, dispatch sheet).",
    )
    samples_parser.add_argument("-r", type=int, default=10, help="Number of records per sample file.")
    samples_parser.add_argument("-o", default=None, help="Output directory path for generated files.")

    ticket_csv_parser = subparsers.add_parser(
        "ticket-csv",
        formatter_class=VDGHelpFormatter,
        help="Generate ticket CSV",
        description="Generate ticket bootstrap/dispatch CSV records.",
    )
    ticket_csv_parser.add_argument("-r", type=int, default=10, help="Number of CSV records to generate.")
    ticket_csv_parser.add_argument("-f", default="generated_records.csv", help="Output CSV filename.")
    ticket_csv_parser.add_argument("-o", default=None, help="Output directory path for generated CSV.")

    api_parser = subparsers.add_parser(
        "crm-api",
        formatter_class=VDGHelpFormatter,
        help="Send CRM ticket API requests",
        description="Authenticate and submit ticket-generation API requests for a VIN range.",
    )
    api_parser.add_argument("-s", type=int, default=40, help="Starting VIN sequence number (inclusive).")
    api_parser.add_argument("-e", type=int, default=45, help="Ending VIN sequence number (inclusive).")
    api_parser.add_argument("-p", default="SURAJ07082025_", help="VIN prefix used to compose VIN_NO values.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "sim-batch":
        generate_sim_batch_csv(num_records=args.r, output_dir=args.o)
    elif args.command == "ticket-json":
        generate_ticket_json(num_records=args.r, output_dir=args.o)
    elif args.command == "fota-batch":
        generate_fota_batch_csv(
            output_file=args.f,
            number_of_records=args.r,
            ufw_version=args.u,
            model=args.m,
            output_dir=args.o,
        )
    elif args.command == "institutional-sales":
        generate_institutional_sales(number_of_records=args.r, output_dir=args.o)
    elif args.command == "sample-files":
        generated_files = generate_all_sample_files(num_records=args.r, output_dir=args.o)
        for key, value in generated_files.items():
            print(f"{key}: {value}")
    elif args.command == "ticket-csv":
        generate_ticket_data_csv(
            number_of_records=args.r,
            output_file=args.f,
            output_dir=args.o,
        )
    elif args.command == "crm-api":
        send_ticket_generation_requests(
            vin_start=args.s,
            vin_end=args.e,
            vin_prefix=args.p,
        )
    else:
        parser.print_help()
        return 1

    return 0
