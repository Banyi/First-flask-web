# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint('main', __name__)  # 创健蓝本

# import放在此处是为了避免蓝本导入循环依赖，views.py, errors.py中也导入main
from . import views, errors
from app.models import Permission

@main.app_context_processor
def inject_permissions():
    """
    使变量在所有模板中全局可访问
    :return:
    """
    return dict(Permission=Permission)