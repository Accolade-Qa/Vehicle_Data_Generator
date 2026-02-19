import random
from datetime import datetime, timedelta


class DynamicFieldFactory:
    def __init__(self, rto_codes: dict[str, list[str]], seed: int | None = None):
        self.rto_codes = rto_codes
        self.rng = random.Random(seed)

    def random_state(self) -> str:
        return self.rng.choice(list(self.rto_codes.keys()))

    def random_rto(self, state: str | None = None) -> tuple[str, str]:
        selected_state = state or self.random_state()
        return selected_state, self.rng.choice(self.rto_codes[selected_state])

    def random_mobile(self, prefix: str = "9") -> str:
        return prefix + "".join(str(self.rng.randint(0, 9)) for _ in range(9))

    def random_registration_number(self) -> str:
        state, rto_code = self.random_rto()
        state_code = rto_code[:2]
        return (
            f"{state_code}"
            f"{self.rng.randint(10, 99)}"
            f"{''.join(self.rng.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))}"
            f"{self.rng.randint(1000, 9999)}"
        )

    def random_pincode(self) -> str:
        return str(self.rng.randint(100000, 999999))

    def random_date(self, start_date: datetime, end_date: datetime, date_format: str) -> str:
        delta = end_date - start_date
        random_days = self.rng.randint(0, delta.days)
        return (start_date + timedelta(days=random_days)).strftime(date_format)
