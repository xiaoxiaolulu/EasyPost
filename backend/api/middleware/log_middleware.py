import ast
import json
from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from utils.logger import logger as logging


class LoggerCollectMiddlewareMixin(MiddlewareMixin):

    def __init__(self, get_response):
        super(LoggerCollectMiddlewareMixin, self).__init__(get_response)

    def log_response(self, request, response):
        """记录服务器响应"""
        content_type = response.get('Content-Type')  # 直接从 response 获取
        block = self._format_headers_log({'Content-Type': content_type}, 'Response')

        if content_type:
            try:
                body = response.content.decode('utf-8')
            except Exception as e:
                body = f"{request.path_info} object has {e}"

            lines = []
            if isinstance(response, HttpResponse):
                lines.extend(f"| {line}" for line in body.splitlines())  # 简化列表生成
            elif isinstance(response, (JsonResponse, Response)):
                try:
                    data = json.loads(body)
                    for k, v in data.items():
                        lines.extend(
                            f"| {k:<15} | {item:<15}"  # 统一格式
                            for item in self._flatten_data(v)
                        )
                except json.JSONDecodeError:
                    lines.extend(f"| {line}" for line in body.splitlines())

            block += '\nBody:\n' + '\n'.join(lines)

        logging.info(block.encode('gbk', 'ignore').decode('gbk'))

    def _flatten_data(self, data):
        """递归展平嵌套数据"""
        if isinstance(data, dict):
            for key, value in data.items():
                yield key
                yield from self._flatten_data(value)
        elif isinstance(data, list):
            for item in data:
                yield from self._flatten_data(item)
        else:
            yield data

    def log_request(self, request):
        """
        记录服务器请求
        """

        request_handler = dict({'REQUEST URL': request.path_info}, **request.META)
        block = 'Request Infomations:\n' + self._format_headers_log(request_handler)

        try:
            request_body = ast.literal_eval(request.body.decode('utf-8'))
        except SyntaxError:
            request_body = request.GET if len(request.GET) else request.POST
        except UnicodeDecodeError:
            block += '+----FileArguments----+\n'
            block += '| {0:<15} | {1:<15} \n'.format(repr("File"), repr(request.body))
        else:

            if request_body:
                block += '+----Arguments----+\n'
                for k, v in request_body.items():
                    block += '| {0:<15} | {1:<15} \n'.format(repr(k), repr(v))

        logging.info(block)

    @staticmethod
    def _format_headers_log(request, format_type: str = 'Headers'):
        """
        格式化日志输出
        """
        # length of '+-...-+' is 19
        block = '+-----Headers-----+\n' if format_type == 'Headers' else '+-----Response-----+\n'

        for k, v in request.items():
            try:
                block += '| {0:<15} | {1:<15} \n'.format(k, v)
            except TypeError:
                block += '| {0:<15} | {1:<15} \n'.format('Undefined', 'Undefined')
        return block

    def process_request(self, request):
        self.log_request(request)

    def process_response(self, request, response):
        self.log_response(request, response)
        return response
