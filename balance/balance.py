import json
import requests
from client import client as c
from typing import Optional
import validation as v

class ResultBalance:
    def __init__(self, type: str, amount: int):
        self.type = type
        self.amount = amount


BALANCE_URI_PATH = "/balance"


class Balance:
    def __init__(self, result: Optional[ResultBalance] = None):
        """
        Initializes a new instance of the Balance class.

        :param result: Optional ResultBalance object containing balance information.
        """
        self.result = result

    def get(client: c.Client):
        """
        Returns the current balance of the account.

        :param client: A Client object containing API authentication details.
        :raises TypeError: If client parameter is not an instance of Client class.
        :return: A Balance object containing the current account balance.
        """
        v.validate([client],[c.Client],"client")
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
