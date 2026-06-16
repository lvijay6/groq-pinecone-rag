import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise EnvironmentError(f"Missing required secret: '{key}'")
    return value
