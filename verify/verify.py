import json
from client import client as c
from typing import List, Optional
import validation as v
import requests

verifyURIPath = "/verify"
verifyACKURIPath = "/verify/acknowledge"
verifyCXLURIPath = "/verify/cancel"

class ResultVerify:
    def __init__(self, request_id: str, number: str, price: float):
        self.request_id = request_id
        self.number = number
        self.price = price


class ResultAcknowledge:
    def __init__(self, request_id: str, price: float):
        self.request_id = request_id
        self.price = price


class ResultCancel:
    def __init__(self, request_id: str):
        self.request_id = request_id


class Params:
    def __init__(self, code_length: Optional[int] = None, language: Optional[str] = None,
                 next_event_wait: Optional[int] = None, pin_expire: Optional[int] = None,
                 from_: Optional[str] = None, tag: Optional[str] = None):
        self.code_length = code_length
        self.language = language
        self.next_event_wait = next_event_wait
        self.pin_expire = pin_expire
        self.from_ = from_
        self.tag = tag


class Verify:
    def __init__(self, result: Optional[ResultVerify] = None):
        """
        Initializes a new instance of the Verify class.

        :param result: Optional ResultVerify object containing verification request information.
        """
        self.result = result
    def send(
        client: c.Client, to: List[str], params: Optional[Params] = None):
        
        """
        Sends a verification request to one or more phone numbers.

        :param client: A Client object containing API authentication details.
        :param to: A list of phone numbers to which the verification code will be sent.
        :param params: Optional Params object containing additional verification request parameters.
        :raises TypeError: If client parameter is not an instance of Client class or if to parameter is not a list.
        :raises ValueError: If to parameter is an empty list.
        :return: A Verify object containing the result of the verification request.
        """
        
        v.validate([client,to],[c.Client,list],["client","to"])
        v.validate_list(to,str,"to")
        if params is None:
            params = Params()

        data = make_send_request_data(client, to, params)

        url = client.endpoint + verifyURIPath
        response = client.request(url, client.content_type_json, data)

        status_code = response["code"]
        body_byte = response["content"]

        if status_code != requests.codes.OK:
            result = json.loads(body_byte)
            error = result["error"]
            return Verify(result=error)

        result = json.loads(body_byte)
        result = ResultVerify(
            request_id=result["request_id"], number=result["number"], price=result["price"])
        return Verify(result=result.__dict__)


def make_send_request_data(client: c.Client, to: List[str], params: Optional[Params] = None) -> dict:
    data = {"api_key": client.api_key,
            "api_secret": client.api_secret, 'to':  ",".join(to)}
    if params is not None:
        if params.code_length is not None:
            data['code_length'] = params.code_length
        if params.language is not None:
            data['language'] = params.language
        if params.next_event_wait is not None:
            data['next_event_wait'] = params.next_event_wait
        if params.pin_expire is not None:
            data['pin_expire'] = params.pin_expire
        if params.from_ is not None:
            data['from'] = params.from_
        if params.tag is not None:
            data['tag'] = params.tag
    return data


class VerifyAcknowledge:
    def __init__(self, result: Optional[ResultAcknowledge] = None):
        """
        Initializes a new instance of the VerifyAcknowledge class.

        :param result: Optional ResultAcknowledge object containing acknowledge information.
        """
        self.result = result

    def send(client: c.Client, requested_id : str, code : str):
        """
        Verify the code entered by the user for the given request ID.

        :param client: A Client object containing API authentication details.
        :param requested_id: A string containing the ID of the request to be acknowledged.
        :param code: A string containing the code to be verified.
        :raises TypeError: If client parameter is not an instance of Client class or if requested_id or code is not a string.
        :raises ValueError: If requested_id or code is empty.
        :return: A VerifyAcknowledge object containing the acknowledge information.
        """
        v.validate([client,requested_id,code],[c.Client,str,str],["client","requested_id","code"])
        data = make_acknowledge_request_data(client,
            request_id=requested_id, code=code)

        url = client.endpoint + verifyACKURIPath
        response = client.request(url, client.content_type_json, data)

        status_code = response["code"]
        body_byte = response["content"]

        if status_code != requests.codes.OK:
            result = json.loads(body_byte)
            error = result["error"]
            return VerifyAcknowledge(result=error)

        result = json.loads(body_byte)
        result = ResultAcknowledge(
            request_id=result["request_id"], price=result["price"])
        return VerifyAcknowledge(result=result.__dict__)


def make_acknowledge_request_data(client:c.Client,request_id: str, code: str) -> dict:
    return {"api_key": client.api_key,
            "api_secret": client.api_secret,
            'request_id': request_id, 'code': code}


class VerifyCancel:
    def __init__(self, result: Optional[ResultCancel] = None):
        """
        Initializes a new instance of the VerifyCancel class.

        :param result: Optional ResultCancel object containing cancelation information.
        """
        self.result = result

    def send(client: c.Client, requested_id):
        """
        Sends a cancelation request for a specific verification request.

        :param client: A Client object containing API authentication details.
        :param requested_id: A string containing the ID of the verification request to be cancelled.
        :raises TypeError: If client parameter is not an instance of Client class, or if requested_id is not a string.
        :raises ValueError: If requested_id is an empty string.
        :return: A VerifyCancel object containing the results of the cancelation request.
        """
        v.validate([client,requested_id],[c.Client,str],["client","requested_id"])
        data = {"api_key": client.api_key,
                "api_secret": client.api_secret, "request_id": requested_id}

        url = client.endpoint + verifyCXLURIPath
        response = client.request(url, client.content_type_json, data)

        status_code = response["code"]
        body_byte = response["content"]

        if status_code != requests.codes.OK:
            result = json.loads(body_byte)
            error = result["error"]
            return VerifyCancel(result=error)

        result = json.loads(body_byte)
        result = ResultCancel(
            request_id=result["request_id"])
        return VerifyCancel(result=result.__dict__)
