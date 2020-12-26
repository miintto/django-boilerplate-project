import os
import json
from django.core.exceptions import ImproperlyConfigured


secret_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(secret_dir, "secrets.json")

class Config:
    with open(path) as f:
        secrets = json.loads(f.read())

    @staticmethod
    def get(key: str) -> dict:
        try:
            return Config.secrets.get(key)
        except:
            raise ImproperlyConfigured
