from typing import Any
import pymysql
from utils.log import log
from contextlib import closing


class OperateMysql(object):

    def __init__(self, connect_setting: dict = None):
        self.connect_setting = connect_setting
        self.conn = None

    def is_connect(self) -> bool:

        try:
            with closing(pymysql.connect(**self.connect_setting)) as conn:
                if isinstance(conn, pymysql.connections.Connection):
                    log.info(f'mysql connect success -> {self.connect_setting.get("db")}')
                    return True
        except Exception as err:
            log.error(f"mysql connect error -> {err}")
            return False
        finally:
            try:
                self.conn.close()
                del self.conn
            except AttributeError:
                pass

    def execute(self, *args, **kwargs) -> None | tuple[Any, ...] | tuple[tuple[Any, ...], ...]:

        conn = pymysql.connect(**self.connect_setting)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(*args, **kwargs)
            conn.commit()
            response = cursor.fetchall()
            if len(response) == 1:
                response = response[0]
            if len(response) == 0:
                response = None
            log.info(f"query mysql result -> {response}")
            return response

        except Exception as err:
            log.error(f"query mysql error -> {err}")
            return None
        finally:
            cursor.close()
            del cursor
            conn.close()
            del conn
