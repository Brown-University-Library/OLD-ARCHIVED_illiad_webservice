# -*- coding: utf-8 -*-

from __future__ import unicode_literals


try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
