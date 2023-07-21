import types
from pathlib import Path
import yaml
from _pytest.python import Module
from requests import request


def pytest_collect_file(file_path: Path, parent):
    if file_path.suffix == ".yaml" and file_path.name.startswith("test"):
        pytest_module = Module.from_parent(parent, path=file_path)
        module = types.ModuleType(file_path.stem)
        raw_dict = yaml.safe_load(file_path.open(encoding='utf-8'))

        for function_name, value in raw_dict.items():
            def function_template(*args, **kwargs):
                for step_key, step_value in value.items():
                    if step_key == 'request':
                        res = request(**step_value)
                    else:
                        eval(step_key)(step_value)

            setattr(module, function_name, function_template)

        pytest_module._getobj = lambda: module
        return pytest_module
