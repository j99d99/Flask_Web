#coding: utf8
from flask import render_template, flash, redirect,request, url_for, session
from forms import LoginUser
from ..models import User
from flask.ext.login import login_required,logout_user,login_user,current_user
from . import auth
from .. import db




@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUser()
    if form.validate_on_submit:
        user = User.query.filter_by(username=form.user_name.data).first()
        if user is not None and user.verify_password(form.user_password.data):
            login_user(user, form.rememberMe.data)
            flash('ok')
            return redirect(request.args.get('next') or url_for('main.hostlist'))
        else:
            flash('error')
    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash(u'退出登录成功')
    return redirect(url_for('auth.login'))
