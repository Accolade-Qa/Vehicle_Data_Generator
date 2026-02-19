import requests

from .settings import SETTINGS


def default_login_payload() -> dict:
    return {"username": SETTINGS.crm_username, "password": SETTINGS.crm_password}


def default_base_payload() -> dict:
    return {
        "ICCID": "89916430934728770133",
        "UIN_NO": "ACON4NA082300008699",
        "DEVICE_IMEI": "861564061408699",
        "DEVICE_MAKE": SETTINGS.device_make,
        "DEVICE_MODEL": "AEPL051401",
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
        "RTO_STATE": "DL",
        "PRIMARY_OPERATOR": "AIRTEL",
        "SECONDARY_OPERATOR": "BSNL",
        "PRIMARY_MOBILE_NUMBER": "8765284847",
        "SECONDARY_MOBILE_NUMBER": "7992635726",
        "VEHICLE_MODEL": "SAFARI",
        "DEALER_CODE": "1133",
        "COMMERCIAL_ACTIVATION_START_DATE": "2025-05-01",
        "COMMERCIAL_ACTIVATION_EXPIRY_DATE": "2028-05-01",
        "MFG_YEAR": "2025",
        "INVOICE_DATE": "2025-05-01",
        "INVOICE_NUMBER": "AEPL18012024-01",
        "CERTIFICATE_VALIDITY_DURATION_IN_YEAR": 2,
    }


def send_ticket_generation_requests(
    vin_start: int = 40,
    vin_end: int = 45,
    vin_prefix: str = "SURAJ07082025_",
    login_api_url: str | None = None,
    vin_api_url: str | None = None,
    login_payload: dict | None = None,
    base_payload: dict | None = None,
):
    login_api_url = login_api_url or SETTINGS.crm_login_api_url
    vin_api_url = vin_api_url or SETTINGS.crm_ticket_api_url
    login_payload = login_payload or default_login_payload()
    base_payload = base_payload or default_base_payload()

    response = requests.post(login_api_url, headers={"Content-Type": "application/json"}, json=login_payload, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(f"Login failed: {response.status_code} | {response.text}")

    token_data = response.json()
    auth_token = token_data.get("authToken") or token_data.get("token")
    if not auth_token:
        raise RuntimeError(f"No token in login response: {token_data}")

    headers = {"token": auth_token, "Content-Type": "application/json"}
    responses = []

    for vin_index in range(vin_start, vin_end + 1):
        payload = base_payload.copy()
        payload["VIN_NO"] = f"{vin_prefix}{vin_index}"
        vin_response = requests.post(vin_api_url, headers=headers, json=[payload], timeout=30)
        responses.append((vin_index, payload["VIN_NO"], vin_response.status_code, vin_response.text))
        print(f"[VIN {vin_index}] VIN_NO: {payload['VIN_NO']} => Status: {vin_response.status_code}")

    return responses
