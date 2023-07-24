import typing as t
from jinja2 import Template, Environment, BaseLoader


def render_template_context(raw: t.Any, *args: t.Any, **kwargs: t.Any) -> str:
    try:
        template = Template(raw, variable_start_string='${', variable_end_string='}')
        ctx = template.render(*args, **kwargs)
        return ctx
    except Exception as err:
        raise PermissionError(f'expression:<{raw}>, error: {err}')


if __name__ == '__main__':
    raw = '''{"url": "http://124.70.221.221:8201/api/v1/login/", "method": "POST", "json": {"statusCode": "13"}}'''

    print(render_template_context(raw, {}))



