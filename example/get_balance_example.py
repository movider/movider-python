from client.client import Client
from balance.balance import Balance


# Replace with your own API key and secret
api_key = "1rpHps23m8lUhu40u4T3hg2ed3W"
api_secret = "9bY1jyW67kJt8pzyzdKngR7ogeG7LmJerTcIXFct"
movider_client = Client(api_key, api_secret)
balance = Balance.get(movider_client)
print(balance.result)