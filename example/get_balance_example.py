from client.client import Client
from balance.balance import Balance


# Replace with your own API key and secret
api_key = "your_api_key"
api_secret = "your_api_secret"
movider_client = Client(api_key, api_secret)
balance = Balance.get(movider_client)
print(balance.result)
