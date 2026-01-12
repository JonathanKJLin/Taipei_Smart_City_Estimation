"""
Celery Configuration
用於異步任務處理
"""
import os
from celery import Celery

# 設定 Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

app = Celery('gov_estimation_system')

# 從 Django settings 載入 Celery 配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自動發現所有 app 中的 tasks
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """測試任務"""
    print(f'Request: {self.request!r}')
