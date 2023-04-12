# Movider Client Library for Python

Movider API client for Python. API support for SMS, Verify, Balance
<img align="right" width="159px" src="https://movider.co/icons/icon-144x144.png">

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

## Installation

Python need to be installed

```bash
  $python
  python 3.10.4
```

Using pip to install package in your projects

```bash
  pip install git+https://github.com/movider/mvd-sdk-python
```

## Usage/Examples

Assuming pip installation worked. You can import the Movider's package like this:

```python
from client.client import Client
```

Then, create a client an instance of Client.

```python
movider_client = Client("your_api_key", "your_api_secret")
```

if you don't have api_key and api_secret, [Sign up](https://dashboard.movider.co/sign-up) Movider's account to use.

## Get Balance

Retreiving current balance in your account.Starting by import the Movider's balance package

```python
from balance.balance import Balance
```

then get the current balance and display it

```python
balance = Balance.get(movider_client)
print(balance.result)
```

## Send SMS

Send an outbound SMS from your Movider's account. Starting by import the Movider's SMS package like this

```python
from sms.sms import Sms
```

then send the sms and display the result

```python
sms = Sms.send(movider_client,["your_recipient_number"],"your_message_to_send")
print(sms.result)
```

your-recipient-number are specified numbers in E.164 format such as 66812345678, 14155552671.

## Documentation

Complete documentation, instructions, and examples are available at [https://movider.co](https://movider.co)

## License

Movider client library for Go is licensed under [The MIT License](./LICENSE). Copyright (c) 2019 1Moby Co.,Ltd
