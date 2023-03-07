from client.client import Client
from sms.sms import Sms


# Replace with your own API key and secret
api_key = "your_api_key"
api_secret = "your_api_secret"
movider_client = Client(api_key, api_secret)
sms = Sms.get_scheduled(movider_client,"your_schedule_id")
print(sms.result)