#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 15:34
# @Author  : Bilon
# @File    : fake.py
import random
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post, Comment


# 生成虚拟用户
def users(count=100):
    fake = Faker(locale='zh_CN')    # 默认为英文，加上locale=zh_CN后为中文
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


# 生成虚拟文章
def posts(count=100):
    fake = Faker()
    # user_count = User.query.count()
    user = User.query.all()
    for i in range(count):
        # u = User.query.offset(randint(0, user_count - 1)).first()
        u = random.choice(user)
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=u)
        db.session.add(p)
    db.session.commit()


# 生成虚拟评论
def comments(count=500):
    fake = Faker()
    user = User.query.all()
    post = Post.query.all()
    for i in range(count):
        u = random.choice(user)
        p = random.choice(post)
        c = Comment(body=fake.text(),
                    timestamp=fake.past_date(),
                    author=u,
                    post=p)
        db.session.add(c)
    db.session.commit()

