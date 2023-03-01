import json
import requests
from client import client
from typing import Optional


class ResultBalance:
    def __init__(self, type: str, amount: int):
        self.type = type
        self.amount = amount


BALANCE_URI_PATH = "/balance"


class Balance:
    def __init__(self, result: Optional[ResultBalance] = None):
        self.result = result

    def get(client: client.Client):
        url = client.endpoint + BALANCE_URI_PATH

        response = client.request(url, client.content_type_json, {"text": ""})
        status_code = response["code"]
        body_byte = response["content"]
        if status_code != requests.codes.OK:
            result = json.loads(body_byte)
            error = result["error"]
            return Balance(result=error)

        result = json.loads(body_byte)
        result = ResultBalance(type=result["type"], amount=result["amount"])
        return Balance(result=result.__dict__)
