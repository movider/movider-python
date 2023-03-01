from client.client import Client
from sms.sms import Sms,Params
from balance.balance import Balance
from verify import verify

# Replace with your own API key and secret
api_key = "1rpHps23m8lUhu40u4T3hg2ed3W"
api_secret = "9bY1jyW67kJt8pzyzdKngR7ogeG7LmJerTcIXFct"

# Create a new Movider client
movider_client = Client(api_key, api_secret)
#test = Sms.sendSchedule(movider_client, to=["+66812345678"],
#                  text="Hello, World!",delivery_datetime="2024-02-01T15:04:05+00:00",params=Params(callback_url="http://example.com/callback"))
test = Balance.get(movider_client)
#test = verify.Verify.send(movider_client,["66812345678"],None)
#test = verify.VerifyAcknowledge.send(movider_client,"jVxKu7E95l7avG8GgQEZwZ16775729786455",code="test")
#test = verify.VerifyCancel.send(movider_client,"jVxKu7E95l7avG8GgQEa6F16775750822139")
#test = Sms.getScheduled(movider_client,135)
#test = Sms.getAllScheduled(movider_client)
#test = Sms.delScheduled(movider_client,131)
print(test.result)