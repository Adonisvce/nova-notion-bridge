# Plugin to call external webhooks

import requests

def trigger_webhook(url, payload):
    response = requests.post(url, json=payload)
    return response.status_code, response.text
