#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 11:09
# @Author  : Bilon
# @File    : __init__.py.py
from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, users, posts, comments, errors
