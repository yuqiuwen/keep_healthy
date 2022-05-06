from django.db import models
from common.model import BaseModel
from users.models import User

# Create your models here.


class Diabetes(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    pregnancies = models.IntegerField(blank=True, null=True, verbose_name='怀孕次数')
    glucose = models.IntegerField(blank=True, null=True, verbose_name='葡萄糖')
    blood_pressure = models.IntegerField(blank=True, null=True, verbose_name='血压')
    skin_thickness = models.IntegerField(blank=True, null=True, verbose_name='皮肤厚度')
    insulin = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name='胰岛素')
    bmi = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='身体质量指数')
    pedigree_function = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True, verbose_name='遗传特性')
    age = models.IntegerField(blank=True, null=True, verbose_name='年龄')
    outcome = models.IntegerField(blank=True, null=True, verbose_name='预测结果,0正常/1发病')
    result = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True, verbose_name='预测患病概率')

    class Meta:
        db_table = 'diabetes'
        verbose_name = '糖尿病数据'
        verbose_name_plural = verbose_name