

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
            self.name = request_body.get('name', None)
            self.url = request_body.get('url', None)
            self.method = request_body.get('method', None)
            self.headers = request_body.get('headers', {})
            self.hooks = request_body.get('hooks', {})
            self.json = request_body.get('json', {})
            self.data = request_body.get('data', {})
            self.params = request_body.get('params', None)
            self.validate = request_body.get('validate', [])
            self.extract = request_body.get('extract', {})

            # 额外参数
            self.gateway = request_body.get('gateway', None)
            self.directory_id = request_body.get('directory_id', None)
            self.project = request_body.get('project', None)
        except (KeyError, ValueError, AttributeError):
            pass
