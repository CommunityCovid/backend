from mysql.connector import Error
from mysql.connector import pooling
import yaml
from yaml import SafeLoader

config_filepath = '../../config.yaml'

# To use connection pool
# 1.first call getConnectionPool to obtain a connection pool.
# 2.Call function get_connection() of connection pool to get a connection

def getConnectionPool():
    database_configs = None
    with open(config_filepath) as config_file:
        config_data = yaml.load(config_file, Loader=SafeLoader)
        database_configs = config_data['database']
    connectionPool = ConnectionPool(database_configs.get("host"),
                                    database_configs.get("database"),
                                    database_configs.get("user"),
                                    database_configs.get("password"),
                                    pool_size=database_configs.get("pool_size"))
    return connectionPool


class ConnectionPool:
    def __init__(self, host, database, user, password, pool_size=2):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.pool_size = pool_size
        self.connection_pool = pooling.MySQLConnectionPool(pool_size=pool_size,
                                                           pool_reset_session=True,
                                                           host=host,
                                                           database=database,
                                                           user=user,
                                                           password=password)

    def get_connection(self):
        try:
            connection = self.connection_pool.get_connection()
            return connection
        except Error as e:
            return None
