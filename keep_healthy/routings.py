from django.urls import re_path

from keep_healthy import consumers

webscoket_urlpatterns = [
    # xxxx/dream/xxx
    re_path(r'/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
