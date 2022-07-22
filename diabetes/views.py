import datetime
import os, sys

from django.db.models import Q, F, Count, Max, Avg
from sklearn.metrics import classification_report,accuracy_score,recall_score,roc_auc_score
import pandas as pd

import traceback
from logger import logger
import json
import pickle
from pandas import read_sql
from concurrent.futures import ThreadPoolExecutor

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.forms.models import model_to_dict
from rest_framework.response import Response
from django_pandas.io import read_frame
from django.db import transaction

from .models import User
from common.http_response import HttpResponse
from common.request import *
from .models import Diabetes
from .serializers import DiabetesModelSerializer

sys.path.append('../')


"""
序列化
create:
    s = DiabetesModelSerializer(data=data)
    s.save()
get:
    diabetes = Diabetes.objects.filter(user=1, is_active=True)
    serializer = DiabetesModelSerializer(diabetes, many=True) #如果查询集有多条，设置many=True
    return response_success("查询成功", serializer.data)
        
update:
    diabetes = Diabetes.objects.get(user=1, is_active=True)
    #instance要更新的对象，partial默认false(需包含所有字段),设置为true表示局部修改
    s = DiabetesModelSerializer(instance=diabetes, data=request.data, partial=False)   
    s.save()

delete:
    #采用逻辑删除，非物理删除，若queryset为单一，则删除一条，否则批量删除
    Diabetes.objects.filter(user=1, is_active=True).update(is_active=False)
"""


threadPool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="diabetes_predict_")


class DiabetesViewSet(ModelViewSet):

    queryset = Diabetes.objects.all()
    serializer_class = DiabetesModelSerializer

    @action(methods=['GET'], detail=False)
    def fetch_diabetes_data(self, request):

        try:
            user = fetch_user(request).id
            diabetes = Diabetes.objects.filter(user=user, is_active=True).order_by('-update_time')
            serializer = DiabetesModelSerializer(diabetes, many=True)
            return HttpResponse.response_success("查询成功", serializer.data)
        except Exception as e:
            logger.error(traceback.format_exc(limit=3))
            return HttpResponse.response_failed("查询失败")

    @action(methods=['POST'], detail=False)
    def start_pred_diabetes(self, request):
        try:
            user = fetch_user(request)
            data = request.data
            # diabetes = Diabetes.objects.create(user=user,
            #                                    pregnancies=data.get('pregnancies'),
            #                                    glucose=data.get('glucose'),
            #                                    blood_pressure=data.get('blood_pressure'),
            #                                    skin_thickness=data.get('skin_thickness'),
            #                                    insulin=data.get('insulin'),
            #                                    bmi=data.get('bmi'),
            #                                    pedigree_function=data.get('pedigree_function'),
            #                                    age=data.get('age'))
            # serializer = DiabetesModelSerializer(diabetes)

            fields = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'pedigree_function', 'age']
            thread = threadPool.submit(self.load_pred_model, request.data, fields=fields)
            result = thread.result()
            if thread.done():
                return HttpResponse.response_success("提交成功", result)

            return HttpResponse.response_success("提交成功")
            # if serializer.is_valid():
            #     serializer.save()
            # print(serializer.is_valid())
            # print(serializer.data)
            # transaction.savepoint_commit(save_id)

        except Exception as e:
            logger.error(traceback.format_exc(limit=3))
            return HttpResponse.response_failed("提交失败")

    def load_pred_model(self, data, fields):
        """
        加载模型
        @param data: queryset
        @param fields: columns
        @return: result
        """
        try:
            # df = read_frame(qs=data, coerce_float=True, fieldnames=fields)
            for k, v in data.items():
                data[k] = [v]
            df = pd.DataFrame.from_dict(data, orient='columns', dtype=float)
            print(df)
            loaded_model = pickle.load(open("./utils/pima.pickle.dat", "rb"))
            y_pred = loaded_model.predict_proba(df)  # 和predict不同的是，predict_proba计算标签概率
            result = list(map(lambda x: '%.3f' % x, y_pred.tolist()[0]))
            print(result)
            return result
        except Exception as e:
            logger.error(traceback.format_exc(limit=3))
            raise e
