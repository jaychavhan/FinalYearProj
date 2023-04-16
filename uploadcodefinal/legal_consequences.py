import requests

API_URL = "https://api-inference.huggingface.co/models/unitary/toxic-bert"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

