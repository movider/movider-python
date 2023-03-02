import json
import requests
# Endpoint points you to Movider REST API.


# ExpectTimeout is used to limit http.Client waiting time.
expect_timeout = 15

class Client:
    """
    A client object that handles API requests to a specific endpoint.

    :param api_key: A string representing the API key for authentication.
    :param api_secret: A string representing the API secret for authentication.
    """
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = "https://mvd-sms-api.ngrok.1mobyline.com/v1"
        self.content_type_json = "application/json"
        self.content_type_xml = "application/xml"
        self.content_type_form_urlencoded = "application/x-www-form-urlencoded"
        self.content_type_form = "multipart/form-data"

    def request(self, url, accept, data):
        """
        Sends a POST request to the specified URL with the given data.

        :param url: A string representing the URL to which the request will be sent.
        :param accept: A string representing the accept header for the request.
        :param data: A dictionary representing the data to be sent in the request body.
        :return: A dictionary containing the response status code and content.
        :raises TypeError: If url, accept or data are not strings or if data is not a dictionary.
        """
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
        """
        Sends a GET request to the specified URL.

        :param url: A string representing the URL to which the request will be sent.
        :param accept: A string representing the accept header for the request.
        :return: A dictionary containing the response status code and content.
        :raises TypeError: If url or accept are not strings.
        """
        headers = {"Accept": accept}
        params = "?api_key=" + self.api_key+"&api_secret=" + self.api_secret
        url += params
        response = requests.get(url, headers=headers)
        return {"code":response.status_code, "content":response.content}
    
    def delete(self,url,accept):
        """
        Sends a DELETE request to the specified URL.

        :param url: A string representing the URL to which the request will be sent.
        :param accept: A string representing the accept header for the request.
        :return: A dictionary containing the response status code and content.
        :raises TypeError: If url or accept are not strings.
        """
        
        headers = {"Accept": accept}
        params = "?api_key=" + self.api_key+"&api_secret=" + self.api_secret
        url += params
        response = requests.delete(url, headers=headers)
        return {"code":response.status_code, "content":response.content}
