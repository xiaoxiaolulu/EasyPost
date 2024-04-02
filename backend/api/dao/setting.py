"""
DESCRIPTION：测试配置数据访问对象
:Created by Null.
"""
import os.path
import typing
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
