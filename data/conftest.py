import types
from pathlib import Path
import yaml
from _pytest.python import Module
from data.engine import PytestRunner


def pytest_collect_file(file_path: Path, parent):

    if file_path.suffix == ".yaml" and file_path.name.startswith("test"):
        pytest_module = Module.from_parent(parent, path=file_path)
        module = types.ModuleType(file_path.stem)
        raw_dict = yaml.safe_load(file_path.open(encoding='utf-8'))

        runner = PytestRunner(raw_dict, module)
        runner.run()

        pytest_module._getobj = lambda: module  # noqa
        return pytest_module
