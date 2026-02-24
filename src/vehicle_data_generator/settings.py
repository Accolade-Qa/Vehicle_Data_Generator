import os
import sys
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv_if_present() -> None:
    candidate_paths: list[Path] = []

    # Source layout (repo root / .env)
    candidate_paths.append(Path(__file__).resolve().parents[2] / ".env")
    # Current working directory
    candidate_paths.append(Path.cwd() / ".env")

    # PyInstaller executable folder and parent folder.
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        candidate_paths.append(exe_dir / ".env")
        candidate_paths.append(exe_dir.parent / ".env")

    # Keep order, remove duplicates.
    seen: set[Path] = set()
    ordered_candidates: list[Path] = []
    for candidate in candidate_paths:
        if candidate not in seen:
            seen.add(candidate)
            ordered_candidates.append(candidate)

    dotenv_path = next((path for path in ordered_candidates if path.exists()), None)
    if dotenv_path is None:
        return

    for line in dotenv_path.read_text(encoding="utf-8").splitlines():
        clean_line = line.strip()
        if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
            continue
        key, value = clean_line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_dotenv_if_present()


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
    crm_username: str = ""
    crm_password: str = ""

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
            crm_username=os.getenv("VDG_CRM_USERNAME", ""),
            crm_password=os.getenv("VDG_CRM_PASSWORD", ""),
        )


SETTINGS = ProjectSettings.from_env()
