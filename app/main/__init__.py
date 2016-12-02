# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint('main', __name__)  # 创健蓝本

# import放在此处是为了避免蓝本导入循环依赖，views.py, errors.py中也导入main
from . import views, errors