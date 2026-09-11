import requests

from config.settings import SETTINGS


def default_login_payload() -> dict:
    if not SETTINGS.crm_username or not SETTINGS.crm_password:
        raise ValueError(
            "CRM credentials are missing. Set VDG_CRM_USERNAME and VDG_CRM_PASSWORD in .env."
        )
    return {"username": SETTINGS.crm_username, "password": SETTINGS.crm_password}


def default_base_payload() -> dict:
    return {
        "ICCID": "89916430934728770133",
        "UIN_NO": "ACON4NA082300008699",
        "DEVICE_IMEI": "861564061408699",
        "DEVICE_MAKE": SETTINGS.device_make,
        "DEVICE_MODEL": SETTINGS.ticket_device_model,
        "ENGINE_NO": "ENGINE_SR_N_30032103",
        "REG_NUMBER": "MH14FF9204",
        "VEHICLE_OWNER_LAST_NAME": "Bhalerao",
        "ADDRESS_LINE_1": "3rd floor,Shantiban Society",
        "ADDRESS_LINE_2": "Behind Walnut School",
        "VEHICLE_OWNER_CITY": "Shivane",
        "VEHICLE_OWNER_DISTRICT": "Pune",
        "VEHICLE_OWNER_STATE": "Maharashtra",
        "VEHICLE_OWNER_COUNTRY": "India",
        "VEHICLE_OWNER_PINCODE": "411045",
        "VEHICLE_OWNER_REGISTERED_MOBILE": "7883841781",
        "POS_CODE": "AB123",
        "POA_DOC_NAME": "PANAB123",
        "POA_DOC_NO": "PAN1AB123",
        "POI_DOC_TYPE": "ADHARAB123",
        "POI_DOC_NO": "ADHARXYZ123",
        "RTO_OFFICE_CODE": "MH14",
        "RTO_STATE": "MH",
        "PRIMARY_OPERATOR": "AIRTEL",
        "SECONDARY_OPERATOR": "BSNL",
        "PRIMARY_MOBILE_NUMBER": "9876543210",
        "SECONDARY_MOBILE_NUMBER": "9876501234",
        "VEHICLE_MODEL": "SUV",
        "DEALER_CODE": "1001",
        "DEVICE_MODEL": SETTINGS.ticket_device_model,
        "MFG_YEAR": 2024,
    }


def send_ticket_generation_requests(vin_start: int, vin_end: int, vin_prefix: str = "") -> list[dict]:
    if vin_start > vin_end:
        raise ValueError("VIN start must be less than or equal to VIN end.")

    responses: list[dict] = []
    for vin_number in range(vin_start, vin_end + 1):
        payload = default_base_payload()
        payload["VIN_NO"] = f"{vin_prefix}{vin_number:05d}"
        response = requests.post(SETTINGS.crm_ticket_api_url, json=payload, timeout=30)
        response.raise_for_status()
        responses.append({"vin": payload["VIN_NO"], "status_code": response.status_code, "body": response.json()})
    return responses
