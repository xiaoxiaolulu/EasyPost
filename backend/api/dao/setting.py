"""
DESCRIPTION：测试配置数据访问对象
:Created by Null.
"""
from unitrunner.database.DBClient import DBClient


class SettingDao:

    @staticmethod
    def database_is_connect(config: dict) -> bool:
        """
        验证数据库连接状态

        Args:
            config: 数据库配置

        Returns: 布尔值

        Raises:
            Exception: 验证数据库连接状态失败时抛出异常
        """
        try:
            db = DBClient()
            ret = db.is_connect(**config)
            return ret
        except (Exception,):
            return False
