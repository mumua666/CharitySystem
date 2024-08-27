# __init__.py:初始化文件 创建Flask应用
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .db import init

# 常见db和app对象


def create():

    # 创建Flask对象app
    app = Flask(__name__)
    # 人为入栈,解决上下文冲突
    ctx = app.app_context()
    ctx.push()
    # 引入数据库配置文件settings.py
    config_path = str(Path('.')/'config'/'settings.py')
    app.config.from_pyfile(config_path)
    # 创建数据库对象db
    db = SQLAlchemy(app)

    return db, app


db, app = create()
__all__ = ['db', 'app', 'init']
