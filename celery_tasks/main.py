# celery启动入口

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keep_healthy.settings')
import django
from celery import Celery
from django.conf import settings


django.setup()



# 创建celery实例对象
celery_app = Celery('healthCenter')

# 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 自动注册异步任务
celery_app.autodiscover_tasks(['celery_tasks.send_email',])
