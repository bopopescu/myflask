#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 18:32
# @Author  : Bilon
# @File    : __init__.py.py

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
