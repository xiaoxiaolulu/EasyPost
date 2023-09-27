import types
from pathlib import Path
import yaml
from _pytest.python import Module
from core.request.engine import PytestRunner
from utils import super_builtins
from utils.log import set_log_format


def pytest_collect_file(file_path: Path, parent):
    if file_path.suffix == ".yaml" and file_path.name.startswith("test"):
        pytest_module = Module.from_parent(parent, path=file_path)
        module = types.ModuleType(file_path.stem)
        raw_dict = yaml.safe_load(file_path.open(encoding='utf-8'))
        print("cccccc")
        print(raw_dict)
        print("cccccc")

        runner = PytestRunner(raw_dict, module)
        runner.run()

        pytest_module._getobj = lambda: module  # noqa
        return pytest_module


def pytest_configure(config):
    set_log_format(config)


def pytest_generate_tests(metafunc):

    params_data = getattr(metafunc.module, 'params_data', None)

    if params_data is not None:
        params_len = len(params_data[0]) if isinstance(params_data, list) else 0

        params_args = metafunc.fixturenames[-params_len:]
        metafunc.parametrize(
            params_args,
            params_data,
            scope="function"
        )


def func1():
    print('-----------------前置条件----------------------')


def func2():
    print('-----------------后置条件----------------------')


super_builtins.func1 = func1
super_builtins.func2 = func2
