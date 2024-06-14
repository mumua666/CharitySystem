from app import db


# 操作日志记录表
class Log(db.Model):
    # 定义表名
    __tablename__ = 'log'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_id = db.Column(db.String(255), unique=False)
    operation_table = db.Column(db.String(255), unique=False, nullable=True)
    operation_name = db.Column(db.String(255), unique=False)
    operation_tuple = db.Column(db.String(255), unique=False, nullable=True)
    log_time = db.Column(db.String(255), unique=False)


# 登陆日志记录表
class LogIn(db.Model):
    # 定义表名
    __tablename__ = "logIn"
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_id = db.Column(db.String(255), unique=False)
    log_time = db.Column(db.String(255), unique=False)
