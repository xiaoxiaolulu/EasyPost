"""
DESCRIPTION：测试配置数据访问对象
:Created by Null.
"""
import builtins
import importlib
import inspect
import os.path
import sys
import traceback
import types
import typing
import uuid
from typing import (
    Any
)
from api.models.setting import Functions
from api.response.fatcory import ResponseStandard
from config.settings import BASE_DIR
from unitrunner.database.DBClient import DBMysql
from unitrunner import builitin
from utils.encoder import parse_string_value
from utils.logger import logger


class SettingDao:

    @staticmethod
    def database_is_connect(config: dict) -> ResponseStandard | dict[str, str | bool]:
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
            db = DBMysql(config)
            ret = db.connect()
            return ret
        except (Exception,):
            pass

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

    def get_function_by_id(self, params: typing.Union[typing.Dict]):
        """
        Retrieves functions based on ID and filters by optional parameters.

        Args:
            params (typing.Union[typing.Dict]): Optional parameters for filtering.
            pk (int): Primary key of the function (0 for all functions).

        Returns:
            dict: A dictionary containing a list of function information and the function mapping.
        """
        if not params.get('id'):
            raise ValueError("参数错误！")

        # Retrieve function content based on ID
        func_info = self.get_func_content(func_key=params.get('id'))

        # Extract content and common content (if available)
        content = func_info.get('content', '')
        common_content = func_info.get('common_content', '')

        # Combine content for function loading
        file_content = content if params.get('id') else common_content  # Use content for specific ID, common content for all

        # Generate unique module name using UUID hash
        module_name = f"{params.get('id')}_{uuid.uuid4().__hash__()}"

        # Load functions from combined content
        functions_mapping = self.load_func_content(f"{common_content}\n{content}", module_name)

        func_list = [
            self.handle_func_info(func)
            for func_name, func in functions_mapping.items()
            if f"def {func_name}(" in file_content  # Check for function definition
               and self.handler_func_list(func, params)  # Apply filtering
               and (not params.get('name') or func_name.__contains__(params.get('name', '')))  # Handle name filtering
        ]

        func_data = {
            'func_list': func_list,
            'functions_mapping': functions_mapping,
        }
        return func_data

    def load_builtin_functions(self) -> typing.Dict[str, typing.Callable]:
        """
        Loads built-in functions from a predefined module (potentially 'builtins').

        Returns:
            typing.Dict[str, typing.Callable]: A dictionary mapping function names to their corresponding functions.
        """
        return self.load_module_functions(builitin)

    def get_mapping_function(
            self, function_name: str, functions_mapping: typing.Dict[str, typing.Callable]
    ) -> typing.Callable:
        """
        Retrieves a function based on its name, searching through various sources.

        Args:
            function_name (str): The name of the function to find.
            functions_mapping (typing.Dict[str, typing.Callable]): A predefined mapping of functions.

        Returns:
            typing.Callable: The retrieved function.

        Raises:
            ModuleNotFoundError: If the function is not found in any of the sources.
        """
        if function_name in functions_mapping:
            return functions_mapping[function_name]

        try:
            built_in_functions = self.load_builtin_functions()
            return built_in_functions[function_name]
        except KeyError:
            pass

        try:
            # check if Python builtin functions
            return getattr(builtins, function_name)
        except AttributeError:
            pass

        raise ModuleNotFoundError(f"函数 {function_name} 没有找到 💔")

    def run_function(self, params: typing.Dict, pk: int) -> typing.Any:
        """
        Runs a function based on its ID and provided parameters.

        Args:
            params (typing.Dict): A dictionary containing function parameters.
            pk (int): The primary key of the function to execute.

        Returns:
            typing.Any: The result of the function execution.

        Raises:
            ValueError: If there are parameter errors, function retrieval fails,
            or function execution encounters errors.
        """

        try:
            # Validate parameters early and concisely
            if not pk or not all(key in params for key in ("func_name", )):
                raise ValueError("参数错误！")

            # Retrieve function information
            params = {**params, **{"id": pk}}
            data = self.get_function_by_id(params)
            functions_mapping = data.get('functions_mapping')
            func = self.get_mapping_function(params.get("func_name"), functions_mapping)

            # Ensure function is found
            if not func:
                raise ValueError('未匹配到函数！')

            # Parse argument values
            args_info = {key: parse_string_value(value) for key, value in params.get('args_info', {}).items()}

            # Execute the function and return the result
            ret = f"{func(**args_info)}\n\t\nProcess finished with exit code 0\n"
            return ret

        except Exception as err:
            raise ValueError(f"函数调试错误：{err}") from err
