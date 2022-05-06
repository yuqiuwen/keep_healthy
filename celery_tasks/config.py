# celery配置文件

broker_url = "redis://auth:{}@localhost:6379/0".format('123456')
result_serializer = 'json'
result_backend = 'django-db'