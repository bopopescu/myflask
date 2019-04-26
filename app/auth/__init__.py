#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/3 11:50
# @Author  : Bilon
# @File    : __init__.py.py
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
