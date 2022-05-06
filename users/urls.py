from django.urls import path
from .views import UserViewSet as users

urlpatterns = [
    path(r'login/', users.as_view({'post': 'login'})),
    path(r'logout/', users.as_view({'post': 'logout'})),
    path(r'send_email/', users.as_view({'post': 'send_email'})),
    path(r'register/', users.as_view({'post': 'register'}))
]
