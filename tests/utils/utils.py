import random
import string
from datetime import datetime, timedelta


def random_datetime() -> datetime:
    return datetime.utcnow() + timedelta(seconds=random.randint(0, 3600))


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))
