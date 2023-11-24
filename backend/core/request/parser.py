

class Format(object):

    def __init__(self, request_body):
        """
        RequestBody => {
            name: 登录1
            request -> {
                url: http://124.70.221.221:8201/api/v1/login/
                method: POST
                headers -> {Content-Type: application/json}
                hooks -> {
                    request_hooks -> [func1]
                    response_hooks -> [func1]
                }
                json -> {}
                data -> {}
                params -> postId=K000612&status=0
            }
            validate -> [{eq: ["$.msg","success"]}]
            extract -> {}
        }
        """
        try:
            # 额外参数
            self.directory_id = request_body.get('directory_id', None)
            self.project = request_body.get('project', None)

            # 基本信息
            self.name = request_body.get('name', None)
            self.url = request_body.get('url', None)
            self.method = request_body.get('method', None)
            self.tags = request_body.get('tags', None)
            self.status = request_body.get('status', None)
            self.desc = request_body.get('desc', None)

            # 请求体
            self.headers = request_body.get('headers', {})
            self.body_type = request_body.get('body_type', 1)
            self.json = request_body.get('json', {})
            self.data = request_body.get('data', {})
            self.params = request_body.get('params', None)
            self.setup_script = request_body.get('setup_script', None)
            self.teardown_script = request_body.get('teardown_script', None)
            self.validate = request_body.get('validate', [])
            self.extract = request_body.get('extract', {})
        except (KeyError, ValueError, AttributeError):
            pass

    def create_step_template(self):
        step_step_template = dict()
        step_step_template['title'] = self.name
        step_step_template['interface']['url'] = self.url
        step_step_template['interface']['name'] = self.name
        step_step_template['interface']['method'] = self.method
        step_step_template['headers'] = self.headers

        match self.body_type:
            case 0:
                step_step_template['request'] = dict()
            case 1:
                step_step_template['request']['json'] = self.json
            case 2:
                step_step_template['request']['data'] = self.data
            case 3:
                step_step_template['request']['params'] = self.params

        step_step_template['setup_script'] = self.setup_script
        step_step_template['teardown_script'] = self.teardown_script
        step_step_template['extract'] = self.extract
        step_step_template['validators'] = self.validate

        step_collection = [{
            'name': '调试接口文档',
            'cases': [step_step_template]
        }]

        return step_collection
