"""
DESCRIPTION：Http(s)请求公共方法封装

:Created by Null.
"""
import datetime
import urllib3
import requests
import simplejson
from urllib import parse
from urllib3.exceptions import InsecureRequestWarning
from core.recursion import GetJsonParams

urllib3.disable_warnings(InsecureRequestWarning)


class HttpHandler(object):

    def __init__(self, request_body: dict):
        self.request_body = request_body

    @staticmethod
    def post(**kwargs: dict) -> requests.Response:
        return requests.post(verify=False, **kwargs)

    @staticmethod
    def get(**kwargs: dict) -> requests.Response:
        return requests.get(verify=False, **kwargs)

    @staticmethod
    def delete(**kwargs: dict) -> requests.Response:
        return requests.delete(verify=False, **kwargs)

    @staticmethod
    def put(**kwargs: dict) -> requests.Response:
        return requests.put(verify=False, **kwargs)

    @staticmethod
    def get_response(response) -> requests.Response:
        try:
            return response.json()
        except simplejson.JSONDecodeError:
            return response.text

    @staticmethod
    def get_elapsed(timer: datetime.timedelta) -> str:
        if timer.seconds > 0:
            return f"{timer.seconds}.{timer.microseconds // 1000}s"
        return f"{timer.microseconds // 100}ms"

    def response(
            self,
            response=None,
            request_body=None,
            elapsed=None,
            msg="success"
    ) -> dict:
        status_code = response.status_code
        response_body = self.get_response(response)
        status = False if response.status_code != 200 else True
        response_headers = [{"name": k, "value": v} for k, v in
                            response.headers.items()] if response.headers is not None else {}
        cookies = [{"name": k, "value": v} for k, v in response.cookies.items()] if response.cookies is not None else {}

        return {
            "status": status,
            "msg": msg,
            "statusCode": status_code,
            "requestBody": request_body,
            "responseHeaders": response_headers,
            "responseBody": response_body,
            "cookies": cookies,
            "cost": elapsed,
            "cookie": response.cookies
        }

    @staticmethod
    def parse_params(request_body) -> dict:
        if request_body['params']:
            if '=' in request_body.get('params') or '&' in request_body.get('params'):
                request_body['params'] = dict(parse.parse_qsl(request_body['params']))
        return request_body

    def request(self) -> dict:
        elapsed = "-1ms"
        method = GetJsonParams.get_value(self.request_body, 'method')
        response = None

        try:
            if method in ['get', 'GET']:
                temp = ('url', 'params', 'headers', 'cookies')
                request_body = GetJsonParams.for_keys_to_dict(*temp, my_dict=self.request_body)
                request_body = self.parse_params(request_body)
                response = self.get(**request_body)

            if method in ['post', 'POST']:
                temp = ('url', 'headers', 'json', 'data', 'files', 'params', 'cookies')
                request_body = GetJsonParams.for_keys_to_dict(*temp, my_dict=self.request_body)
                request_body = self.parse_params(request_body)
                response = self.post(**request_body)

            elapsed = self.get_elapsed(response.elapsed)
            return self.response(response, self.request_body, elapsed)

        except Exception as e:
            return self.response(response, self.request_body, elapsed, msg=str(e))
