# 定义数据库连接时各个字段
USERNAME='root'
PASSWORD='123456'
HOSTNAME = '172.23.232.111'
PORT='3306'
DATABASE='CharitySystem'

# 配置URL
# 格式： mysql+pymysql://USERNAME:PASSWORD@HOSTNAME:PORT/DATABASE
DB_URI='mysql+pymysql://{}:{}@{}:{}/{}'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    PORT,
    DATABASE
)


# MySQL数据库地址
SQLALCHEMY_DATABASE_URI = DB_URI
# 是否跟踪对象修改
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 是否回显SQL语句
SQLALCHEMY_ECHO = True
# session加密的随机秘钥
SECRET_KEY = '123456'
