import importlib
import inspect
import json
import os
from string import Template
import jinja2
import jsonpath
import pytest
import requests
import yaml


def all_functions():
    """加载debug.py模块"""
    debug_module = importlib.import_module("data.debug")
    all_function = inspect.getmembers(debug_module, inspect.isfunction)
    # print(dict(all_function))
    return dict(all_function)


def pytest_collect_file(parent, file_path):
    if file_path.suffix == ".yaml" and file_path.name.startswith("test"):
        return YamlFile.from_parent(parent, path=file_path)


class YamlFile(pytest.File):
    def collect(self):
        import yaml
        yml_raw = self.fspath.open(encoding='utf-8').read()
        yml_var = Template(yml_raw).safe_substitute(os.environ)
        yml_var = jinja2.Template(yml_var).render(**all_functions())
        raw = yaml.safe_load(yml_var)

        for yaml_case in raw:
            name = yaml_case["test"]["name"]
            values = yaml_case["test"]
            yield YamlItem.from_parent(self, name=name, spec=values)


class YamlItem(pytest.Item):
    def __init__(self, name, parent, spec):
        super().__init__(name, parent)
        self.name = name
        self.values = spec
        self.request = self.values.get("request")
        self.validate = self.values.get("validate")
        self.s = requests.session()
        self._obj = None

    def values_render_variable(self, values):
        # 替换测试用例中的关联值
        yaml_test = Template(json.dumps(values)).safe_substitute(os.environ)
        values = yaml.safe_load(yaml_test)
        return values

    def runtest(self):
        values = self.values_render_variable(self.values)
        request_data = values["request"]
        print(request_data)
        response = self.s.request(**request_data)

        self.assert_response(response, self.validate)

        if values.get("extract"):
            for key, value in values.get("extract").items():
                os.environ[key] = jsonpath.jsonpath(response.json(), value)[0]
        self.assert_response(response, values.get("validate"))

    def assert_response(self, response, validate):
        """自定义断言"""
        for i in validate:
            if "eq" in i.keys():
                yaml_result = i.get("eq")[0]
                actual_result = jsonpath.jsonpath(response.json(), yaml_result)
                expect_result = i.get("eq")[1]

                assert actual_result[0] == expect_result
