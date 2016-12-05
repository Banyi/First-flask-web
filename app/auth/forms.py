# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1,64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Username must have only letters,'
                                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in user.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password =  PasswordField('New password', validators=[DataRequired(), EqualTo('password2', 'Password must match.')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('New Password', validatord=[DataRequired(),
                                                         EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')

class ChangeEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')