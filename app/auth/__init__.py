# -*- coding: utf-8 -*-

from flask import Blueprint

auth = Blueprint('auth', __name__)

from app.main import views