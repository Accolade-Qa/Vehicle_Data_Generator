# VDG CLI

This project generates multiple vehicle-data artifacts (CSV, JSON, XLSX) and can also call the CRM ticket API.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

Optional environment configuration:

```powershell
Copy-Item .env.example .env
```

Set CRM values in `.env` before using `crm-api`:
- `VDG_CRM_USERNAME`
- `VDG_CRM_PASSWORD`

## CLI Usage

Run as a CLI:

```powershell
vdg --help
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
vdg sim-batch -r 20 -o output
vdg ticket-json -r 5 -o output
vdg fota-batch -r 10 -f fota_batch.csv -u 5.2.9 -m 4G -o output
vdg institutional-sales -r 15 -o output
vdg sample-files -r 10 -o output
vdg ticket-csv -r 25 -f generated_records.csv -o output
vdg crm-api -s 40 -e 45 -p SURAJ07082025_
```

Help:

```powershell
vdg -h
vdg <command> -h
```

## Dynamic Field Design

Dynamic field generation is centralized in `src/vehicle_data_generator/dynamic_fields.py` via `DynamicFieldFactory`.
Modules consume this class for random/stateful fields like:

- RTO and state
- registration number
- mobile numbers
- pincodes
- random date generation

Settings are centralized in `src/vehicle_data_generator/settings.py` and can be overridden via environment variables.
