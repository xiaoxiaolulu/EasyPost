from contextlib import closing
import MySQLdb
from utils.log import log


class DBMysql:
    """mysql databases"""

    def __init__(self, config):
        config['autocommit'] = True
        self.con = MySQLdb.connect(**config)
        self.cur = self.con.cursor(MySQLdb.cursors.DictCursor)

    def execute(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchone()

    def execute_all(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def __del__(self):
        self.cur.close()
        self.con.close()


class DBClient:

    def init_connect(self, DB): # noqa
        if isinstance(DB, dict):
            self.create_db_connect(DB)
        else:
            for config in DB:
                self.create_db_connect(config)

    def create_db_connect(self, config):
        if not config:
            return
        if not config.get('name'):
            raise ValueError('数据库配置的name字段不能为空！')

        if config.get('type').lower() == 'mysql' and config.get('config'):
            dbc = DBMysql(config.get('config'))
        else:
            raise ValueError('您传入的数据库配置有误，或者apin目前不支持：{}'.format(config))

        setattr(self, config.get('name'), dbc)

    def close_connect(self):
        """断开连接"""
        for db in list(self.__dict__.keys()):
            delattr(self, db)

    def is_connect(self, config) -> bool:

        try:
            with closing(MySQLdb.connect(**config)) as conn:

                if isinstance(conn, MySQLdb.connections.Connection):
                    log.info(f'mysql connect success -> {config.get("db")}')
                    return True
        except Exception as err:
            log.error(f"mysql connect error -> {err}")
            return False
        finally:
            try:
                self.close_connect()
            except AttributeError:
                pass
