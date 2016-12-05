# -*- coding:utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class Role(db.Model):
    __tablename__ = 'roles'  # 表名
    # 字段定义
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(64), unique=True)  # 唯一值约束
    users = db.relationship('User', backref='role', lazy='dynamic')  # 关系一个角色对应多个用户,一对多

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 将两个模型建立关联关系
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """
        利用itsdangerous生成确认令牌,Serializer()接收config['SECRET_KEY']是一个秘钥，
        dumps()指定数据生成一个加密签名，然后对数据和签名进行序列化，生成令牌字符串
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """
        解码令牌，检验签名和过期时间，若通过返回原始数据
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change-password') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return Flase
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        return True

    def __repr__(self):
        return '<User %r>' % self.username



@login_manager.user_loader
def load_user(user_id):
    """
    通过回调加载用户
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))