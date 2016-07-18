# -*- coding: utf-8 -*-
"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import os

PKG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(PKG_PATH, "data")
PLUGIN_PATH = os.path.normpath(os.path.join(PKG_PATH, os.pardir, "plugins"))

CONFIG_PATH = os.path.normpath(os.path.join(PKG_PATH, os.pardir))

def config(*fname):
    return os.path.join(CONFIG_PATH, *fname)

def data(*fname):
    return os.path.join(DATA_PATH, *fname)

LOG_FILE = '/tmp/xuebao.log'
KEYWORD = u'雪宝'
