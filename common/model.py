from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='删除标记')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # 只用来继承，并不创建表