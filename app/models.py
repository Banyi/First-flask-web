# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app import db


class Role(db.Model):
    __tablename__ = 'roles'  # 表名
    # 字段定义
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(64), unique=True)  # 唯一值约束
    users = db.relationship('User', backref='role', lazy='dynamic')  # 关系一个角色对应多个用户,一对多

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 将两个模型建立关联关系

    def __repr__(self):
        return '<User %r>' % self.username