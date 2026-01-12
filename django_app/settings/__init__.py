"""
Django Settings Module
根據環境變數 DJANGO_ENV 載入對應的設定
"""
import os

# 預設使用開發環境設定
env = os.environ.get('DJANGO_ENV', 'dev')

if env == 'prod':
    from .prod import *
else:
    from .dev import *
