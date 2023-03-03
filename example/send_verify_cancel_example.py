from client.client import Client
from verify.verify import VerifyCancel


# Replace with your own API key and secret
api_key = "your_api_key"
api_secret = "your_api_secret"
movider_client = Client(api_key, api_secret)
verify = VerifyCancel.send(movider_client,"your_requested_id")
print(verify.result)