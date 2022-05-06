from django.db import models
from django.contrib.auth.models import AbstractUser
from common.model import BaseModel

# Create your models here.


class User(AbstractUser):
    sexType = (('M', 'male'), ('F', 'Female'))
    roles = models.IntegerField(default=1, verbose_name='角色')
    code = models.CharField(max_length=256, null=True,blank=True, verbose_name='邮箱验证码')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='注册提交时间')
    is_remember = models.BooleanField(default=False, verbose_name='是否记住登录状态')
    sex = models.CharField(max_length=1, choices=sexType, null=True, blank=True)


    class Meta:
        db_table = 'users'
        ordering = ["-c_time"]
        verbose_name = '用户管理表'
        verbose_name_plural = verbose_name


# class PersonHealthData(BaseModel):
#
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
#     pregnancies = models.IntegerField(blank=True, null=True, verbose_name='怀孕次数')
#     glucose = models.IntegerField(blank=True, null=True, verbose_name='葡萄糖')
#     blood_pressure = models.IntegerField(blank=True, null=True, verbose_name='血压')
#     skin_thickness = models.IntegerField(blank=True, null=True, verbose_name='皮肤厚度')
#     insulin = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name='胰岛素')
#     pedigree_function = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True, verbose_name='遗传特性')
#     age = models.IntegerField(blank=True, null=True, verbose_name='年龄')
#     outcome = models.IntegerField(blank=True, null=True, verbose_name='预测结果,0正常/1发病')
#     height = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name='身高,单位cm')
#     weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name='体重,单位kg')
#
#
#
#     class Meta:
#         db_table = 'diabetes'
#         verbose_name = '糖尿病数据'
#         verbose_name_plural = verbose_name