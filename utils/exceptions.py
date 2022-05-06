from rest_framework.views import exception_handler as drf_exception_handle
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger('django')


def exception_handler(exc, context):
    """
    自定义异常处理
    @param exc: 异常实例对象
    @param context: 抛出异常的上下文
    @return:
    """
    response = drf_exception_handle(exc, context)

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            logger.error('[{}] {}'.format(view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
