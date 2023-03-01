import json
from typing import List, Optional

import requests

from client import client


class Params:
    def __init__(
        self,
        callback_url: Optional[str] = None,
        callback_method: Optional[str] = None,
        from_: Optional[str] = None,
    ):
        self.callback_url = callback_url
        self.callback_method = callback_method
        self.from_ = from_


class PhoneNumber:
    def __init__(self, number: str, message_id: str, price: float):
        self.number = number
        self.message_id = message_id
        self.price = price


class BadNumber:
    def __init__(self, number: str, msg: str):
        self.number = number
        self.msg = msg


class ResultSms:
    def __init__(
        self,
        remaining_balance: float,
        total_sms: int,
        phone_number_list: List[PhoneNumber],
        bad_phone_number_list: List[BadNumber],
        scheduled_id: Optional[int] = None
    ):
        self.remaining_balance = remaining_balance
        self.total_sms = total_sms
        self.phone_number_list = phone_number_list
        self.bad_phone_number_list = bad_phone_number_list
        self.scheduled_id = scheduled_id


class ResultSchedule:
    def __init__(self, id: int, text: str, total_sms: int, method: str, callback_url: str,
                 from_number: str, delivery_date: str, delivery_status: str, delivery_status_update_date: str,
                 created_date: str):
        self.id = id
        self.text = text
        self.total_sms = total_sms
        self.method = method
        self.callback_url = callback_url
        self.from_number = from_number
        self.delivery_date = delivery_date
        self.delivery_status = delivery_status
        self.delivery_status_update_date = delivery_status_update_date
        self.created_date = created_date


SMS_URI_PATH = "/sms"
SMS_SCHEDULE_URI_PATH = "/sms/scheduled"


class Sms:
    def __init__(self, result: Optional[ResultSms] = None):
        self.result = result
    def send(
        client: client.Client, to: List[str], text: str, params: Optional[Params] = None
    ):
        if len(to) == 0:
            raise ValueError("at least 1 receiver is required.")

        if not text:
            raise ValueError("text is required.")

        if params is None:
            params = Params()

        data = make_request_data(client, to, text, params=params)

        url = client.endpoint + SMS_URI_PATH
        response = client.request(url, client.content_type_form, data)

        status_code = response["code"]
        body_byte = response["content"]
        if status_code != requests.codes.OK:
            result = json.loads(body_byte)
            error = result["error"]
            return Sms(result=error)
        result = json.loads(body_byte)
        result = result_sms_from_json(result)
        return Sms(result=result.__dict__)

    def sendSchedule(
        client: client.Client, to: List[str], text: str, delivery_datetime: str, params: Optional[Params] = None
    ):
        if len(to) == 0:
            raise ValueError("at least 1 receiver is required.")

        if not text:
            raise ValueError("text is required.")

        if not delivery_datetime:
            raise ValueError("date time is required")

        if params is None:
            params = Params()

        data = make_request_data(client, to, text, delivery_datetime, params)

        url = client.endpoint + SMS_SCHEDULE_URI_PATH
        response = client.request(url, client.content_type_form, data)
        status_code = response["code"]
        body_byte = response["content"]
        if status_code != requests.codes.OK:
            result = json.loads(body_byte)
            error = result["error"]
            return Sms(result=error)

        result = json.loads(body_byte)
        result = result_sms_from_json(result)
        return Sms(result=result.__dict__)

    def getScheduled(client: client.Client, schedule_id):
        url = client.endpoint + SMS_SCHEDULE_URI_PATH + "/"+str(schedule_id)
        response = client.get(url, client.content_type_json)
        status_code = response["code"]
        body_byte = response["content"]
        if status_code != requests.codes.OK:
            result = json.loads(body_byte)
            error = result["error"]
            return Sms(result=error)

        result = json.loads(body_byte)
        result = result_schedule_from_json(result)
        return Sms(result=result.__dict__)

    def getAllScheduled(client: client.Client):
        url = client.endpoint + SMS_SCHEDULE_URI_PATH
        response = client.get(url, client.content_type_json)
        status_code = response["code"]
        body_byte = response["content"]
        if status_code != requests.codes.OK:
            result = json.loads(body_byte)
            error = result["error"]
            return Sms(result=error)

        result = json.loads(body_byte)
        result_list = []
        for item in result["items"]:
            result_list.append(result_schedule_from_json(item).__dict__)

        return Sms(result=result_list)
    
    def delScheduled(client: client.Client,schedule_id):
        url = client.endpoint + SMS_SCHEDULE_URI_PATH + "/"+str(schedule_id)
        response = client.get(url, client.content_type_json)
        status_code = response["code"]
        body_byte = response["content"]
        if status_code != requests.codes.OK:
            result = json.loads(body_byte)
            error = result["error"]
            return Sms(result=error)

        return Sms(result="Delete Complete")


def make_request_data(
    client: client.Client, to: List[str], text: str, delivery_datetime: Optional[str] = None, params: Optional[Params] = None
) -> dict:
    data = {
        "api_key": client.api_key,
        "api_secret": client.api_secret,
        "to": ",".join(to),
        "text": text,
        "callback_url": params.callback_url,
        "callback_method": params.callback_method,
        "from": params.from_,
    }
    if delivery_datetime:
        data["delivery_datetime"] = delivery_datetime
    return data


def result_sms_from_json(data: dict) -> ResultSms:
    phone_number_list = [
        PhoneNumber(number=pn["number"],
                    message_id=pn["message_id"], price=pn["price"]).__dict__
        for pn in data["phone_number_list"]
    ]
    bad_phone_number_list = [
        BadNumber(number=bpn["number"], msg=bpn["msg"]).__dict__
        for bpn in data["bad_phone_number_list"]
    ]
    result_sms = ResultSms(
        remaining_balance=data["remaining_balance"],
        total_sms=data["total_sms"],
        phone_number_list=phone_number_list,
        bad_phone_number_list=bad_phone_number_list,
    )
    if data["scheduleId"]:
        result_sms.scheduled_id = data["scheduleId"]

    return result_sms


def result_schedule_from_json(data: dict) -> ResultSchedule:
    return ResultSchedule(
        id=data["id"],
        text=data["text"],
        total_sms=data["total_sms"],
        method=data["method"],
        callback_url=data["callback_url"],
        from_number=data["from"],
        delivery_date=data["delivery_date"],
        delivery_status=data["delivery_status"],
        delivery_status_update_date=data["delivery_status_updated_date"],
        created_date=data["created_date"]
    )
