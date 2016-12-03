# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswrodField, BooleanField, SubmitField
from wtforms.validators import DateRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DateRequired(), Length(1,64), Email()])
    password = PasswrodField('Password', validators=[DateRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')