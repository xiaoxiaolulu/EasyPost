from typing import Any
from api.models.https import (
    Api
)
from api.models.project import Project
from core.engine.session_runner import (
    run_test,
    run_api
)
from core.request.parser import HandelTestData


class HttpDao:

    @staticmethod
    def parser_api_data(request: Any):

        api = HandelTestData(request.data) # noqa

        request_body = {
            'name': api.name,
            'project': Project.objects.get(id=api.project),
            'directory_id': api.directory_id,
            'method': api.method,
            'url': api.url,
            'tags': api.tags,
            'status': api.status,
            'desc': api.desc,
            'headers': api.headers,
            'raw': api.raw,
            'params': api.params,
            'setup_script': api.setup_script,
            'teardown_script': api.teardown_script,
            'validate': api.validate,
            'extract': api.extract,
            'user': request.user
        }
        try:
            return request_body
        except (Exception, ):
            raise Exception("解析测试接口失败")

    @classmethod
    def create_or_update_api(cls, request: Any, pk):
        try:
            request_body = cls.parser_api_data(request)
            if pk:
                update_obj = Api.objects.filter(id=pk)
                update_obj.update(**request_body)
                update_pk = pk
            else:
                create_obj = Api.objects.create(**request_body)
                update_pk = create_obj.id

            return update_pk
        except Exception as e:
            raise Exception(f"{e}")

    @classmethod
    def run_api_doc(cls, api: dict):

        try:
            api = HandelTestData(api)
            api_data = api.get_api_template()
            result = run_api(api_data=api_data)
            return result
        except Exception as e:
            raise Exception(f"调试测试接口失败: {e}")
