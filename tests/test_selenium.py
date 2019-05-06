#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/28 9:57
# @Author  : Bilon
# @File    : test_selenium.py
import re
import threading
import unittest
from selenium import webdriver

from app import create_app, db, fake
from app.models import Role, User


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # 启动Chrome
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')    # 用谷歌浏览器的无头模式（没有界面）
        try:
            cls.client = webdriver.Chrome(chrome_options=options)
        except:
            pass    # 如果无法启动浏览器则跳过这些测试

        if cls.client:
            # 创建程序
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # 禁止日志，保持输出简洁
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            # 创建数据库，并生成一些虚拟数据
            # db.drop_all() # 如果有脏数据，先清空
            # db.session.remove()
            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            # 添加管理员
            admin_role = Role.query.filter_by(name='Administrator').first()
            admin = User(email='john@example.com',
                         username='john', password='cat',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # 在一个线程中启动Flask服务起
            threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # 关闭Flask服务器和浏览器
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            # 销毁数据库
            db.drop_all()
            db.session.remove()

            # 删除程序上下文
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('无法启动浏览器')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # 进入首页
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger\s+!', self.client.page_source))

        # 进入登录页面
        self.client.find_element_by_link_text('Sign in').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)

        # 登录
        # self.client.find_element_by_id('email').send_keys('john@example.com')
        # self.client.find_element_by_id('password').send_keys('cat')
        # self.client.find_element_by_id('submit').click()
        # self.assertTrue(re.search('Hello,\s+john\s+!', self.client.page_source))

        # 进入用户个人资料页面
        # self.client.find_element_by_link_text('Profile').click()
        # self.assertTrue('<h1>john</h1>' in self.client.page_source)
