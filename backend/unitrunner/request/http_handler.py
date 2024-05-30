"""
DESCRIPTION：Http(s)请求公共方法封装

:Created by Null.
"""
import datetime
import json
import urllib3
import requests
import simplejson
from urllib import parse
from urllib3.exceptions import InsecureRequestWarning
from unitrunner.engine.env import session
from utils.recursion import GetJsonParams


urllib3.disable_warnings(InsecureRequestWarning)


class HttpHandler(object):

    def __init__(self, request_body: dict):
        self.request_body = request_body

    @staticmethod
    def get_response(response) -> requests.Response:
        try:
            response_body = response.json()
            response_body = json.dumps(response_body, ensure_ascii=False, indent=2)
            return response_body
        except simplejson.JSONDecodeError:
            response_body = response.content
            response_body = response_body.decode('utf-8') if response_body else ''
            return response_body

    @staticmethod
    def get_request(response) -> requests.Response:
        try:
            requests_body = json.loads(response.request.body.decode('utf-8'))
            requests_body = json.dumps(requests_body, ensure_ascii=False, indent=2)
            return requests_body
        except (Exception,):
            requests_body = response.request.body
            requests_body = requests_body or ''
            return requests_body

    @staticmethod
    def get_elapsed(timer: datetime.timedelta) -> str:
        if timer.seconds > 0:
            return f"{timer.seconds}.{timer.microseconds // 1000}s"
        return f"{timer.microseconds // 100}ms"

    def response(
            self,
            response=None,
            elapsed=None,
            msg="success"
    ) -> dict:
        status_code = response.status_code
        response_body = self.get_response(response)
        request_body = self.get_request(response)
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

    def request(self):
        elapsed = "-1ms"
        method = GetJsonParams.get_value(self.request_body, 'method')
        response = None

        try:
            # if method in [HttpMethodEnum.GET_LOWER, HttpMethodEnum.GET_UPPER]:
                # temp = ('url', 'params', 'headers', 'cookies')
                # request_body = GetJsonParams.for_keys_to_dict(*temp, my_dict=self.request_body)
                # request_body = self.parse_params(request_body)
                # response = self.get(**self.request_body)

            # if method in [HttpMethodEnum.POST_LOWER, HttpMethodEnum.POST_UPPER]:
                # temp = ('url', 'headers', 'json', 'data', 'files', 'params', 'cookies')
                # request_body = GetJsonParams.for_keys_to_dict(*temp, my_dict=self.request_body)
                # request_body = self.parse_params(request_body)
                # response = self.post(**self.request_body)

            # elapsed = self.get_elapsed(response.elapsed)
            # return self.response(response, self.request_body, elapsed)
            response = session.request(**self.request_body)
            return response
        except Exception as e:
            raise ValueError('❌请求发送失败，错误信息如下：{}'.format(e))
