"""
DESCRIPTION：测试配置数据访问对象
:Created by Null.
"""
import importlib
import inspect
import os.path
import sys
import traceback
import types
import typing
import uuid
from typing import (
    Dict,
    Any
)
from api.models.setting import Functions
from config.settings import BASE_DIR
from unitrunner.database.DBClient import DBClient
from utils.logger import logger


class SettingDao:

    @staticmethod
    def database_is_connect(config: dict) -> bool:
        """
        This static method checks if a database connection can be established
        using the provided configuration.

        Args:
            config: A dictionary containing database connection details.
            Expected keys may include:
                - host: The hostname or IP address of the database server.
                - port: The port number of the database server.
                - username: The username for database access.
                - password: The password for database access.
                (and potentially others depending on your database system)

        Returns:
            True if the connection is successful, False otherwise.
        """
        try:
            db = DBClient()
            ret = db.is_connect(**config)
            return ret
        except (Exception,):
            return False

    @staticmethod
    def handle_function_content(func_key: typing.Union[int, str, None]) -> typing.Dict:
        """
        This static method retrieves the content of a built-in function from the database
        based on the provided function key.

        Args:
            func_key: The primary key of the function in the database. This can be an integer,
            a string, or None.

        Returns:
            A dictionary containing the function's content.

        Raises:
            Exception: If an error occurs while retrieving the function content.
        """
        try:
            func_info = Functions.objects.get(pk=func_key)
            content = func_info.content
            return content
        except (Functions.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取内置函数内容失败 -> {err}"
            )
            raise Exception("获取内置函数内容失败❌")

    @staticmethod
    def get_common_content() -> str:
        """
        Retrieves common content from a file, handling potential errors gracefully.

        Returns:
            The contents of the file as a string, or an empty string if the file
            cannot be read due to errors.
        """

        func_path = os.path.join(BASE_DIR, 'unitrunner', 'builitin', 'functions.py')

        try:
            with open(func_path, encoding='utf8') as file:
                return file.read()
        except (FileNotFoundError, PermissionError) as e:
            # Log or handle specific errors explicitly
            logger.warning(f"Failed to read common content from {func_path}: {e}")
            return ""
        except Exception as e:
            # Handle unexpected errors more generally
            logger.error(f"Unexpected error reading common content: {e}")
            return ""

    def get_func_content(self, func_key: typing.Union[int, str, None]) -> typing.Dict:
        """
        Retrieves the content for a built-in function and combines it with common content.

        Args:
            func_key: The primary key of the function in the database. This can be an integer,
                     a string, or None.

        Returns:
            A dictionary containing the combined content:
                - content: Function content retrieved from the database using `handle_function_content`.
                - common_content: Common content loaded from a separate file using `get_common_content`.
        """
        content = self.handle_function_content(func_key)
        common_content = self.get_common_content()
        return {
            'content': content,
            'common_content': common_content
        }

    @staticmethod
    def function_save_or_update(params: typing.Union[typing.Dict], pk: int) -> typing.Dict[typing.Text, typing.Any]:
        """
        Creates or updates a built-in function record in the database.

        Args:
            params: A dictionary containing the function data to be created or updated.
            pk: The primary key of the function to be updated. If None, a new record is created.

        Returns:
            A dictionary containing:
                - update_pk: The primary key of the created or updated function record.

        Raises:
            ValueError: If the provided params are not a valid dictionary.
            Exception: If an error occurs during the create or update operation.
        """
        if not isinstance(params, dict):
            raise ValueError("更新参数错误！")
        else:
            try:
                if pk:
                    update_obj = Functions.objects.filter(id=pk)
                    update_obj.update(**params)
                    update_pk = pk
                else:
                    create_obj = Functions.objects.create(**params)
                    update_pk = create_obj.id

                return update_pk
            except Exception as err:
                logger.debug(
                    f"🏓编辑内置函数数据失败 -> {err}"
                )
                raise Exception(f"{err} ❌")

    @staticmethod
    def load_module_functions(module) -> typing.Dict[str, typing.Callable]:
        """
        Loads all functions defined within a given module into a dictionary.

        Args:
            module: The module object containing the functions to be loaded.

        Returns:
            A dictionary where the keys are function names and the values are the corresponding
            function objects.
        """
        module_functions = {}

        for name, item in vars(module).items():
            if isinstance(item, types.FunctionType):
                module_functions[name] = item

        return module_functions

    def load_func_content(self, content: str, module_name: str) -> typing.Dict[str, typing.Callable]:
        """
        Loads function content from a string, creates a temporary module, and returns its functions.

        Args:
            content: The string containing the function definitions.
            module_name: The name to assign to the temporary module.

        Returns:
            A dictionary containing the names and callable objects of the loaded functions.

        Raises:
            IndentationError: If the provided content has indentation errors.
            ModuleNotFoundError: If importing the temporary module fails.
            Exception: If any other errors occur during the process.
        """
        mod = sys.modules.setdefault(module_name, types.ModuleType(module_name))
        try:
            code = compile(content, module_name, 'exec')
            exec(code, mod.__dict__)
            imported_module = importlib.import_module(module_name)
        except IndentationError:
            raise IndentationError(f"格式错误，请检查！\n {traceback.format_exc()}")
        except ModuleNotFoundError:
            raise ModuleNotFoundError(f"模块导入错误！\n {traceback.format_exc()}")
        except Exception:
            raise Exception(f"脚本错误！\n {traceback.format_exc()}")

        module_functions = self.load_module_functions(imported_module)
        return module_functions

    def edit_builtin_function(self, params: typing.Union[typing.Dict], pk: int) -> dict[str, Any]:
        """
        Edits a built-in function, handling shared content and saving updates.

        Args:
            params (typing.Dict[str, Any]): Input parameters for the function.
            pk (int): Primary key of the function to be edited.

        Returns:
            dict[str, Any]: Response from the function save/update operation.
        """
        content = self.get_common_content()
        params['content'] = content
        self.load_func_content(content=content, module_name=uuid.uuid4().hex)
        response = self.function_save_or_update(params, pk=pk)

        return response

    @staticmethod
    def handle_func_info(func: types.FunctionType) -> typing.Dict:
        """
        Extracts and organizes information about a given function.

        Args:
            func (types.FunctionType): The function to inspect.

        Returns:
            typing.Dict: A dictionary containing the extracted function information.
        """
        func_info = inspect.signature(func)
        parameters = func_info.parameters
        args_dict = dict()
        for name, param_info in parameters.items():
            args_dict.setdefault(name, param_info.default if not isinstance(param_info.default, type) else '')

        return dict(
            func_name=func.__name__,
            func_args=str(func_info),
            args_info=args_dict,
            func_doc=func.__doc__,
        )

    @staticmethod
    def handler_func_list(func: types.FunctionType, params: typing.Union[typing.Dict]):
        """
        Checks if a function should be included in the list based on optional filtering parameters.

        Args:
            func (types.FunctionType): The function to be evaluated.
            params (typing.Union[typing.Dict]): Optional dictionary containing filtering parameters.

        Returns:
            bool: True if the function should be included, False otherwise.
        """

        condition = not params.get('func_name') or any(
            search_term in (func.__name__, func.__doc__ or '')  # Use docstring or an empty string
            for search_term in [params.get('func_name'), ]
        )
        return condition

    def get_function_by_id(self, params: typing.Union[typing.Dict], pk: int):
        """
        Retrieves functions based on ID and filters by optional parameters.

        Args:
            params (typing.Union[typing.Dict]): Optional parameters for filtering.
            pk (int): Primary key of the function (0 for all functions).

        Returns:
            dict: A dictionary containing a list of function information and the function mapping.
        """
        if not pk:
            raise ValueError("参数错误！")

        # Retrieve function content based on ID
        func_info = self.get_func_content(func_key=pk)

        # Extract content and common content (if available)
        content = func_info.get('content', '')
        common_content = func_info.get('common_content', '')

        # Combine content for function loading
        file_content = content if pk else common_content  # Use content for specific ID, common content for all

        # Generate unique module name using UUID hash
        module_name = f"{pk}_{uuid.uuid4().__hash__()}"

        # Load functions from combined content
        functions_mapping = self.load_func_content(f"{common_content}\n{content}", module_name)

        func_list = []
        for func_name, func in functions_mapping.items():
            # Early termination if function definition is absent
            if file_content.find(f'def {func_name}(') == -1:
                continue

            # Concisely filter based on search terms and handle potential absence of a docstring
            if self.handler_func_list(func, params):
                func_list.append(self.handle_func_info(func))

        func_data = {
            'func_list': func_list,
            'functions_mapping': functions_mapping,
        }
        return func_data
