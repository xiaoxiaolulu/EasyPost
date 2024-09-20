"""
DESCRIPTION：Http(s)请求公共方法封装

:Created by Null.
"""
import datetime
import json
import socket
import time
from typing import Union
import urllib3
import requests
import simplejson
from urllib3.exceptions import InsecureRequestWarning
from unitrunner import exceptions
from unitrunner.engine.env import session


urllib3.disable_warnings(InsecureRequestWarning)


class HttpHandler(object):

    def __init__(self, request_body: dict = None):
        self.request_body = request_body

    @staticmethod
    def get_response(response: requests.Response) -> Union[str, dict]:
        """
        Extracts the response body from the provided Response object.

        This function attempts to decode the response body as JSON. If successful,
        it converts the data to a dictionary using `json.dumps` with proper formatting
        and returns the dictionary. Otherwise, it decodes the raw content as UTF-8 and returns
        the raw bytes as a string.

        Args:
            response (requests.Response): The Response object containing the HTTP response.

        Returns:
            Union[str, dict]: The response body as either a formatted JSON string or raw bytestring.
        """

        try:
            response_body = response.json()
            response_body = json.dumps(response_body, ensure_ascii=False, indent=2)
            return response_body
        except simplejson.JSONDecodeError:
            response_body = response.content
            response_body = response_body.decode('utf-8') if response_body else ''
            return response_body

    @staticmethod
    def get_request(response: requests.Response) -> Union[str, dict]:
        """
        Extracts the request body from the provided Response object.

        This function attempts to decode the request body as JSON. If successful,
        it converts the data to a dictionary using `json.loads` and returns the dictionary
        with proper formatting. Otherwise, it returns the raw bytestring of the request body
        as a string.

        Args:
            response (requests.Response): The Response object containing the HTTP response.

        Returns:
            Union[str, dict]: The request body as either a formatted JSON string or raw bytestring.
        """
        try:
            requests_body = response.request.body
            if isinstance(requests_body, bytes):
                requests_body = json.loads(response.request.body.decode('utf-8'))
                requests_body = json.dumps(requests_body, ensure_ascii=False, indent=2)
            return requests_body
        except exceptions.GetRequestException:
            requests_body = response.request.body
            requests_body = requests_body or ''
            return requests_body

    @staticmethod
    def get_elapsed(timer: datetime.timedelta) -> str:
        """
        Formats a datetime.timedelta object into a human-readable time string.

        This function takes a `datetime.timedelta` object representing an elapsed time
        and converts it into a string that is easier for humans to understand. The format
        used depends on the magnitude of the elapsed time.

        Args:
            timer (datetime.timedelta): The timedelta object representing the elapsed time.

        Returns:
            str: The formatted elapsed time string (e.g., "5.234s" or "123ms").
        """
        if timer.seconds > 0:
            return f"{timer.seconds}.{timer.microseconds // 1000}s"
        return f"{timer.microseconds // 100}ms"

    @staticmethod
    def measure_dns_resolution(host: str) -> float:
        """Measures the DNS resolution time for a given host.

        Args:
            host (str): The hostname to resolve.

        Returns:
            float: The DNS resolution time in seconds.
        """
        try:
            start_time = time.time()
            socket.getaddrinfo(host, None)
            end_time = time.time()
            dns_resolution_time = (end_time - start_time) * 1000
            return dns_resolution_time
        except exceptions.DnsConnectException as err:
            raise exceptions.TcpConnectException('❌Dns连接失败，错误信息如下：{}'.format(err))

    @staticmethod
    def measure_tcp_connection_time(host: str) -> float:
        """Measures the TCP connection time for a given host.

        Args:
            host (str): The hostname to connect to.

        Returns:
            float: The TCP connection time in seconds.

        Raises:
            TcpConnectException: If the connection fails.
        """
        start_time = time.time()
        try:
            sock = socket.create_connection((host, 80))
            sock.close()
            end_time = time.time()
            connection_time = (end_time - start_time) * 1000
            return connection_time
        except exceptions.TcpConnectException as err:
            raise exceptions.TcpConnectException('❌Tcp连接失败，错误信息如下：{}'.format(err))

    def response(
            self,
            response: requests.Response = None,
            elapsed: datetime.timedelta = None,
            msg: str = "success"
    ) -> dict:
        """
        Constructs a dictionary containing response information.

        This function takes a `requests.Response` object (optional), an elapsed time
        `datetime.timedelta` object (optional), and a message string (optional). It processes
        the response object (if provided) to extract relevant data like status code, response body,
        request body, headers, and cookies. It then constructs a dictionary containing these
        details, along with the provided message and elapsed time.

        Args:
            response (requests.Response, optional): The Response object containing the HTTP response details.
                Defaults to None.
            elapsed (datetime.timedelta, optional): The timedelta object representing the elapsed time.
                Defaults to None.
            msg (str, optional): A message string to be included in the response. Defaults to "success".

        Returns:
            dict: The constructed dictionary containing response information.
        """
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

    def request(self) -> requests.Response:
        """
        Sends the HTTP request using the provided request data.

        This function attempts to send the HTTP request using the `session` object and the request data
        stored in the `self.request_body` attribute. If the request is successful, it returns the
        `requests.Response` object containing the response details. Otherwise, it catches any exceptions
        and raises a `ValueError` with an error message indicating the failure.

        Returns:
            requests.Response: The HTTP response object if the request is successful.
        Raises:
            ValueError: If an exception occurs during the request.
        """
        try:
            response = session.request(**self.request_body)
            return response
        except exceptions.SendRequestException as err:
            raise exceptions.SendRequestException('❌请求发送失败，错误信息如下：{}'.format(err))
