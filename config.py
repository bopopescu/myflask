#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 17:48
# @Author  : Bilon
# @File    : config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))    #__file__为当前脚本文件


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Hard2Guess'   # 秘钥

    FLASKY_ADMIN = 'dongpiquo@gmail.com'

    # 数据库相关配置
    SQLALCHEMY_TRACK_MODIFICATIONS = True   # 非必填
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True    # 自动提交

    # 邮件相关配置
    MAIL_SERVER = 'smtp.qq.com'  # 邮件服务器地址
    # MAIL_PORT = 25    # 邮件服务器端口,默认25
    # MAIL_USE_TLS = True   # 启用传输层安全
    MAIL_USERNAME = '1551658080@qq.com'  # 邮件服务账号
    MAIL_PASSWORD = 'wbawewprwmlthffa'  # 密码
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'  # 邮件标题前面部分
    FLASKY_POSTS_PER_PAGE = 10  # 每页显示博客条数
    FLASKY_FOLLOWERS_PER_PAGE = 10 # 每页显示关注者个数
    FLASKY_COMMENTS_PER_PAGE = 10    # 每页显示评论数

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost:3306/flask'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost:3306/flasktest'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost:3306/flask'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
