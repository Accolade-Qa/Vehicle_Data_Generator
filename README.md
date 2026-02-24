# Vehicle Data Generator (Desktop App + EXE)

This project generates multiple vehicle-data artifacts (CSV, JSON, XLSX) and can call the CRM ticket API.
It now runs as a desktop software app and can be packaged into a Windows `.exe`.

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

Set CRM values in `.env` before using CRM API actions:
- `VDG_CRM_USERNAME`
- `VDG_CRM_PASSWORD`

## Run as Desktop Software (No CLI Required)

```powershell
python -m vehicle_data_generator
```

Or, if installed in the active environment:

```powershell
vdg
```

The app opens a GUI where you can:
- generate SIM batch CSV
- generate ticket JSON
- generate FOTA batch CSV
- generate institutional sales XLSX
- generate sample files
- generate ticket CSV
- send CRM ticket API requests

## Build Windows EXE

Use the included build script:

```powershell
.\build_exe.ps1
```

Optional clean build:

```powershell
.\build_exe.ps1 -Clean
```

Output executable:

```text
dist\VehicleDataGenerator.exe
```

Run it directly:

```powershell
.\dist\VehicleDataGenerator.exe
```
