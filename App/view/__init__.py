# views.py: 路由 + 视图函数

from flask import Blueprint, request, render_template, jsonify, Response, redirect, url_for
from model import *

# 创建蓝图
blue = Blueprint('user', __name__)