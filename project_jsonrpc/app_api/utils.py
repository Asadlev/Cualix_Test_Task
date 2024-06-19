import json
import requests
from django.conf import settings


def call_jsonrpc(method, params=None):
    url = "https://slb.medv.ru/api/v2/"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": 1
    }

    cert = (settings.CLIENT_CERT, settings.CLIENT_KEY)

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, cert=cert)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        return {"error": str(error)}



