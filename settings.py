import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectSettings:
    default_output_dir: str = "output"
    device_make: str = "ACCOLADE"
    device_model_4g: str = "ACON4NA"
    ticket_device_model: str = "AEPL051400"
    default_fota_ufw: str = "5.2.8_TST03"
    default_fota_model: str = "4G"

    crm_login_api_url: str = "http://20.219.88.214:6109/api/crm/generateToken"
    crm_ticket_api_url: str = "http://20.219.88.214:6109/api/crm/generateTickets"
    crm_username: str = "accoladeCrm"
    crm_password: str = "admin@123"

    @classmethod
    def from_env(cls) -> "ProjectSettings":
        return cls(
            default_output_dir=os.getenv("VDG_DEFAULT_OUTPUT_DIR", "output"),
            device_make=os.getenv("VDG_DEVICE_MAKE", "ACCOLADE"),
            device_model_4g=os.getenv("VDG_DEVICE_MODEL_4G", "ACON4NA"),
            ticket_device_model=os.getenv("VDG_TICKET_DEVICE_MODEL", "AEPL051400"),
            default_fota_ufw=os.getenv("VDG_DEFAULT_FOTA_UFW", "5.2.8_TST03"),
            default_fota_model=os.getenv("VDG_DEFAULT_FOTA_MODEL", "4G"),
            crm_login_api_url=os.getenv("VDG_CRM_LOGIN_API_URL", "http://20.219.88.214:6109/api/crm/generateToken"),
            crm_ticket_api_url=os.getenv("VDG_CRM_TICKET_API_URL", "http://20.219.88.214:6109/api/crm/generateTickets"),
            crm_username=os.getenv("VDG_CRM_USERNAME", "accoladeCrm"),
            crm_password=os.getenv("VDG_CRM_PASSWORD", "admin@123"),
        )


SETTINGS = ProjectSettings.from_env()
