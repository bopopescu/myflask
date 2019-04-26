#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/3 11:51
# @Author  : Bilon
# @File    : views.py
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ChangeEmailForm, \
    PasswordResetRequestForm, PasswordResetForm
from ..email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        # flash('You can now login.')
        # return redirect(url_for('auth.login'))
        db.session.commit()     # 只有提交数据库后才能够得到新用户id，而生成token需要用到用户id，所以需要添加db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirm email has been send to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('confirm/<token>')
@login_required     # 让一个路由仅让认证的用户能访问，未认证用户访问，Flask-Login会拦截请求，把用户发往登录页面
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


# @auth.before_app_request    # 蓝本中的程序全局请求钩子
# def before_request():
#     # 如果当前用户已登录and帐号未激活and请求端点不在认证蓝本中and不是静态文件,则跳转到unconfirmed页面
#     if current_user.is_authenticated:
#         # 如果登录就更新最后访问时间
#         current_user.ping()
#
#         # 如果帐号未激活and请求端点不在认证蓝本中,则跳转到unconfirmed页面
#         if not current_user.confirmed and request.endpoint[:5] != 'auth.':
#             return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    # 如果是匿名用户or帐号已激活则正常跳转，否则跳转到unconfirmed页面
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required     # 让一个路由仅让认证的用户能访问，未认证用户访问，Flask-Login会拦截请求，把用户发往登录页面
def resend_confirmation():
    # 重新发送确认邮件
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A confirm email has been send to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required     # 让一个路由仅让认证的用户能访问，未认证用户访问，Flask-Login会拦截请求，把用户发往登录页面
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required     # 让一个路由仅让认证的用户能访问，未认证用户访问，Flask-Login会拦截请求，把用户发往登录页面
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password', 'auth/email/reset_password', user=user, token=token)
        flash('An email with instructions to reset your password has been sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address', 'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change_email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
