import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

_cache = {}

def get_secret(key: str) -> str:
    # Local dev — read from .env
    value = os.environ.get(key)
    if value:
        return value

    # AWS Lambda — read from Secrets Manager
    if key not in _cache:
        secret_name = os.environ.get("AWS_SECRET_NAME", "agentic-ai-secrets")
        client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))
        response = client.get_secret_value(SecretId=secret_name)
        _cache.update(json.loads(response["SecretString"]))

    if key not in _cache:
        raise EnvironmentError(f"Missing required secret: '{key}'")
    return _cache[key]
