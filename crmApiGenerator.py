import requests


DEFAULT_LOGIN_API_URL = "http://20.219.88.214:6109/api/crm/generateToken"
DEFAULT_VIN_API_URL = "http://20.219.88.214:6109/api/crm/generateTickets"


DEFAULT_LOGIN_PAYLOAD = {
    "username": "accoladeCrm",
    "password": "admin@123",
}


DEFAULT_BASE_PAYLOAD = {
    "ICCID": "89916430934728770133",
    "UIN_NO": "ACON4NA082300008699",
    "DEVICE_IMEI": "861564061408699",
    "DEVICE_MAKE": "ACCOLADE",
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
    vin_start=40,
    vin_end=45,
    vin_prefix="SURAJ07082025_",
    login_api_url=DEFAULT_LOGIN_API_URL,
    vin_api_url=DEFAULT_VIN_API_URL,
    login_payload=None,
    base_payload=None,
):
    login_payload = login_payload or DEFAULT_LOGIN_PAYLOAD
    base_payload = base_payload or DEFAULT_BASE_PAYLOAD

    login_headers = {"Content-Type": "application/json"}
    resp_login = requests.post(login_api_url, headers=login_headers, json=login_payload)

    if resp_login.status_code != 200:
        raise RuntimeError(f"Login failed: {resp_login.status_code} | {resp_login.text}")

    token_data = resp_login.json()
    auth_token = token_data.get("authToken") or token_data.get("token")
    if not auth_token:
        raise RuntimeError(f"No token in login response: {token_data}")

    print(f"Login successful. Token received.")

    vin_headers = {
        "token": auth_token,
        "Content-Type": "application/json",
    }

    responses = []
    for i in range(vin_start, vin_end + 1):
        payload = base_payload.copy()
        payload["VIN_NO"] = f"{vin_prefix}{i}"
        resp_vin = requests.post(vin_api_url, headers=vin_headers, json=[payload])
        responses.append((i, payload["VIN_NO"], resp_vin.status_code, resp_vin.text))
        print(f"[VIN {i}] VIN_NO: {payload['VIN_NO']} => Status: {resp_vin.status_code}")

    return responses
