import types
from pathlib import Path
import pytest
import yaml
from _pytest.python import Module
from core.request.engine import PytestRunner
from utils.log import set_log_format


def pytest_collect_file(file_path: Path, parent):
    if file_path.suffix == ".yaml" and file_path.name.startswith("test"):
        pytest_module = Module.from_parent(parent, path=file_path)
        module = types.ModuleType(file_path.stem)
        raw_dict = yaml.safe_load(file_path.open(encoding='utf-8'))

        runner = PytestRunner(raw_dict, module)
        runner.run()

        pytest_module._getobj = lambda: module  # noqa
        return pytest_module


def pytest_configure(config):
    set_log_format(config)


test_data = [{"test_input": "3+5",
              "expected": 8,
              "id": "验证3+5=8"
              },
             {"test_input": "2+4",
              "expected": 6,
              "id": "验证2+4=6"
              },
             {"test_input": "6 * 9",
              "expected": 54,
              "id": "验证6*9=54"
              }
             ]


def pytest_generate_tests(metafunc):
    ids = []
    if "parameters" in metafunc.fixturenames:
        for data in test_data:
            ids.append(data['id'])  # ids 表示测试用例的编号
        metafunc.parametrize("parameters", test_data, ids=ids, scope="function")


@pytest.fixture(scope="function")
def requests_function(request):
    pass
