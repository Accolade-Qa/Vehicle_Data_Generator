# Vehicle Data Generator CLI

This project generates multiple vehicle-data artifacts (CSV, JSON, XLSX) and can also call the CRM ticket API.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Optional environment configuration:

```powershell
Copy-Item .env.example .env
```

Set CRM values in `.env` before using `crm-api`:
- `VDG_CRM_USERNAME`
- `VDG_CRM_PASSWORD`

## CLI Usage

Run as a module:

```powershell
python -m Vehicle_data_generator --help
```

### Commands

- `sim-batch`: Generate SIM batch CSV
- `ticket-json`: Generate ticketing JSON
- `fota-batch`: Generate FOTA CSV
- `institutional-sales`: Generate institutional sales XLSX
- `sample-files`: Generate sample-format files
- `ticket-csv`: Generate ticket CSV
- `crm-api`: Send CRM ticket API requests

Examples:

```powershell
python -m Vehicle_data_generator sim-batch --records 20
python -m Vehicle_data_generator ticket-json --records 5 --output-dir output
python -m Vehicle_data_generator fota-batch --records 10 --ufw 5.2.9 --model 4G
python -m Vehicle_data_generator institutional-sales --records 15
python -m Vehicle_data_generator sample-files --records 10
python -m Vehicle_data_generator ticket-csv --records 25
python -m Vehicle_data_generator crm-api --vin-start 40 --vin-end 45 --vin-prefix SURAJ07082025_
```

## Dynamic Field Design

Dynamic field generation is centralized in `Vehicle_data_generator/dynamic_fields.py` via `DynamicFieldFactory`.
Modules consume this class for random/stateful fields like:

- RTO and state
- registration number
- mobile numbers
- pincodes
- random date generation

Settings are centralized in `Vehicle_data_generator/settings.py` and can be overridden via environment variables.
