# -*- coding:utf-8 -*-

from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, \
    current_app, make_response
from app.main import main
from .forms import NameForm
from app import db
from app.models import User, Role
from app.auth import auth


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
            flash('You changed the name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))  # 修改后重定向为main.index
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())


@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# @auth.route('/login')
# def login():
#     return render_template('auth/login.html')