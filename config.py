# -*- coding: utf-8 -*-

import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    CSRF_ENABLED = True
    SSL_DISABLE = False
    DATABASE = r'd:\Demo\App\flaskr.db'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'  # 跨站请求伪造保护
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[flasky]'
    FLASKY_MAIL_SENDER = 'Flask Admin <flask@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASK_ADMIN')
    MAIL_PORT = 587
    MAIL_USE_TIL = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # 数据库URL必须保存到这个键中
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}