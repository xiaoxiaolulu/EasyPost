from contextlib import closing
import MySQLdb
from utils.logger import logger as log


class DBMysql:
    """mysql databases"""

    def __init__(self, config):
        """
        Initializes the database connection.

        This is the constructor method for a class (likely named something relevant to database interaction).
        It takes a configuration dictionary (`config`) as input and establishes a connection to a MySQL database.

        Args:
            config (dict): A dictionary containing configuration parameters for the database connection.
            The expected keys in the dictionary are:
                - host (str): The hostname or IP address of the MySQL server.
                - user (str): The username for the database connection.
                - password (str): The password for the database connection.
                - db (str): The name of the database to connect to.
                (Optional) - autocommit (bool): Whether to enable autocommit mode (defaults to True).
        """
        config['autocommit'] = True
        self.con = MySQLdb.connect(**config)
        self.cur = self.con.cursor(MySQLdb.cursors.DictCursor)

    def execute(self, sql):
        """
        Executes a SQL query and returns the first row of the result.

        This method executes the provided SQL query (`sql`) on the database connection established by the object.
        It then fetches the first row of the result set and returns it as a dictionary.

        Args:
            sql (str): The SQL query to execute.

        Returns:
            dict: The first row of the result set as a dictionary, or None if no rows were returned.
        """
        self.cur.execute(sql)
        return self.cur.fetchone()

    def execute_all(self, sql):
        """
        Executes a SQL query and returns all rows of the result.

        This method executes the provided SQL query (`sql`) on the database connection established by the object.
        It then fetches all rows of the result set and returns them as a list of dictionaries.

        Args:
            sql (str): The SQL query to execute.

        Returns:
            list: A list of dictionaries representing all rows of the result set.
        """
        self.cur.execute(sql)
        return self.cur.fetchall()

    def __del__(self):
        """
        Destructor method to close the database connection.

        This method is called automatically when the object is garbage collected.
        It ensures that the database cursor and connection objects are properly closed to release resources.
        """
        self.cur.close()
        self.con.close()


class DBClient:

    def init_connect(self, DB): # noqa
        """
        Initializes database connections based on input configuration.

        This method accepts either a single database configuration dictionary (`DB`)
        or a list of configuration dictionaries. It creates and stores database connections
        for each provided configuration using the `create_db_connect` method.

        Args:
            DB (dict or list): A dictionary containing a single database configuration
                or a list of database configuration dictionaries.
                Each configuration dictionary is expected to have keys for host, user, password, and db.
        """
        if isinstance(DB, dict):
            self.create_db_connect(DB)
        else:
            for config in DB:
                self.create_db_connect(config)

    def create_db_connect(self, config):
        """
        Creates a database connection object based on the provided configuration.

        This method validates the configuration dictionary (`config`) and creates a
        corresponding database connection object. It currently only supports MySQL connections.

        Args:
            config (dict): A dictionary containing database configuration details.

            Expected keys include:
                - name (str): A unique identifier for this connection within the object.
                - type (str): The type of database (currently only 'mysql' is supported).
                - config (dict, optional): The specific configuration for the database type
                    (e.g., host, user, password, db for MySQL).

        Raises:
            ValueError:
                - If the configuration dictionary is empty.
                - If the 'name' field is missing or empty.
                - If the database type is not supported or the 'config' dictionary is missing for MySQL.
        """
        if not config:
            return
        if not config.get('name'):
            raise ValueError('The name field of the database configuration cannot be empty!❌')

        if config.get('type').lower() == 'mysql' and config.get('config'):
            dbc = DBMysql(config.get('config'))
        else:
            raise ValueError('The database configuration you passed in is incorrect：{} ❌'.format(config))

        setattr(self, config.get('name'), dbc)

    def close_connect(self):
        """
        Closes all database connections associated with the object.

        This method iterates through all attributes of the object and calls `delattr`
        to delete those attributes that are database connections. This effectively closes
        the connections and releases their resources.

        Assumes that database connections are stored as attributes of the object.
        Typically used when connections are no longer needed or to avoid resource leaks.
        """
        for db in list(self.__dict__.keys()):
            delattr(self, db)

    def is_connect(self, config) -> bool:
        """
        Checks if a connection to a MySQL database can be established with the provided configuration.

        This method attempts to connect to a MySQL database using the given configuration dictionary (`config`).
        It uses a context manager (`closing`) to ensure the connection is properly closed regardless of
        success or failure.

        Args:
            config (dict): A dictionary containing the database configuration details.
                Expected keys include host, user, password, and db.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            with closing(MySQLdb.connect(**config)) as conn:

                if isinstance(conn, MySQLdb.connections.Connection):
                    log.info(f'mysql connect success -> {config.get("db")} ✅')
                    return True
        except Exception as err:
            log.error(f"mysql connect error -> {err} ❌")
            return False
        finally:
            try:
                self.close_connect()
            except AttributeError:
                pass


if __name__ == '__main__':
    db = DBClient()
    ret = db.is_connect(
        {
            'database': 'easypost',
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456'
        }
    )
    print(ret)
