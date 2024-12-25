import os


FASTAPI_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
JWT_KEY = os.environ.get('JET_KEY', '17610855585')


CHECK_DB_DRIVER = os.getenv('DB_DRIVER', 'postgres')
CHECK_DB_HOST = os.getenv('DB_HOST', '10.10.10.21')
CHECK_DB_PORT = os.getenv('DB_PORT', 3307)
CHECK_DB_DATABASE = os.getenv('DB_DATABASE', 'appagora')
CHECK_DB_USERNAME = os.getenv('DB_USERNAME', 'root')
CHECK_DB_PASSWORD = os.getenv('DB_PASSWORD', 'Admin911$')
CHECK_SQLALCHEMY_MYSQL_URL = 'postgres+pymysql://' + CHECK_DB_USERNAME + ':' + CHECK_DB_PASSWORD + '@' + CHECK_DB_HOST + ':' + str(CHECK_DB_PORT) + '/' + CHECK_DB_DATABASE + '?charset=utf8mb4'
SQLALCHEMY_POSTGRESQL_URL = "postgresql://user:password@postgresserver/db"
