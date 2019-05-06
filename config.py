#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 17:48
# @Author  : Bilon
# @File    : config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))    #__file__为当前脚本文件


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Hard2Guess'   # 秘钥

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
    FLASKY_MAIL_SENDER = 'Flasky Admin <1551658080@qq.com>'
    FLASKY_ADMIN = 'dongpiquo@gmail.com'    # 管理员邮件地址

    FLASKY_POSTS_PER_PAGE = 10  # 每页显示博客条数
    FLASKY_FOLLOWERS_PER_PAGE = 10 # 每页显示关注者个数
    FLASKY_COMMENTS_PER_PAGE = 10    # 每页显示评论数

    SQLALCHEMY_RECORD_QUERIES = True    # 启用 '记录查询统计' 功能
    FLASKY_SLOW_DB_QUERY_TIME = 0.5  # 设置缓慢查询的上限值为0.5秒

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

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # 把错误通过电子邮件发送给管理员
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN, '30884413@qq.com'],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' 程序出现错误',
            credentials=credentials,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)




config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
