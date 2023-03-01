import json
import requests
# Endpoint points you to Movider REST API.


# ExpectTimeout is used to limit http.Client waiting time.
expect_timeout = 15


class Client:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = "https://mvd-sms-api.ngrok.1mobyline.com/v1"
        self.content_type_json = "application/json"
        self.content_type_xml = "application/xml"
        self.content_type_form_urlencoded = "application/x-www-form-urlencoded"
        self.content_type_form = "multipart/form-data"

    def request(self, url, accept, data):
        headers = {
            "Content-Type": self.content_type_form_urlencoded,
            "Accept": accept
        }
        params = "?api_key=" + self.api_key+"&api_secret=" + self.api_secret
        url += params
        response = requests.post(url, headers=headers,
                                 data=data, timeout=expect_timeout)
        return {"code":response.status_code, "content":response.content}

    def get(self, url, accept):
        headers = {"Accept": accept}
        params = "?api_key=" + self.api_key+"&api_secret=" + self.api_secret
        url += params
        response = requests.get(url, headers=headers)
        return {"code":response.status_code, "content":response.content}
    
    def delete(self,url,accept):
        headers = {"Accept": accept}
        params = "?api_key=" + self.api_key+"&api_secret=" + self.api_secret
        url += params
        response = requests.delete(url, headers=headers)
        return {"code":response.status_code, "content":response.content}
