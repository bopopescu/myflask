#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 18:34
# @Author  : Bilon
# @File    : forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError
from flask_pagedown.fields import PageDownField

from app.models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# 普通用户修改信息表单
class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    avatar = FileField('头像')
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


# 管理员修改信息表单
class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, '用户名只能包含字母数字和下划线')])
    confirmed = BooleanField('Confirmed')

    # SelectField实例必须在其choices属性中设置各选项,选项必须是一个由元组组成的列表，各元组都包含两个元素：选项的标识符和显示在控件中的文本字符串
    # choices列表在表单的构造函数(__init__)中设定,其值从Role模型中获取,使用一个查询按照角色名的字母顺序排列所有角色
    # 元组中的标识符是角色的id,因为这是个整数,所以在SelectField构造函数中添加coerce=int参数,把字段值转换为整数,而不使用默认的字符串
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


# 博客帖子表单
class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


# 评论输入表单
class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
