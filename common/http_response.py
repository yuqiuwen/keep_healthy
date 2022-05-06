from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.status import *

HTTP_SUCCESS = 'APP0001'
HTTP_ERROR = 'APP0000'


class HttpResponse(Response):

    def __init__(self, data_status='', message='', results=None, status=None, headers=None, exception=False, **kwargs):
        data = {
            'code': data_status,
            'msg': message
        }
        if results is not None:
            data['results'] = results
        data.update(kwargs)
        super().__init__(data=data, status=status, headers=headers, exception=exception)

    @classmethod
    def response_success(cls, message='', data=None):
        return HttpResponse(HTTP_200_OK, message=message, results=data,status=HTTP_200_OK)

    @classmethod
    def response_failed(cls, message='', data=None):
        return HttpResponse(HTTP_500_INTERNAL_SERVER_ERROR, message=message, results=data, status=HTTP_500_INTERNAL_SERVER_ERROR)


def result(code='', message='', data=None, kwargs=None):
    json_dict = {
        'data': data,
        'code': code,
        'msg': message
    }
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict, json_dumps_params={'ensure_ascii': False})
