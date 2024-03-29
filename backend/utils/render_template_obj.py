import typing as t
from jinja2 import Template


def render_template_context(raw: t.Any, *args: t.Any, **kwargs: t.Any) -> str:
    try:
        template = Template(raw, variable_start_string='${{', variable_end_string='}}')
        ctx = template.render(*args, **kwargs)
        return ctx
    except Exception as err:
        raise PermissionError(f'expression:<{raw}>, error: {err}')


if __name__ == '__main__':

    raw = {
        "name": "hello",
        "username": ""
    }
    ext = {"username": "xxxx"}
    r = render_template_context(f'''{raw}''', **ext)
    print(r)