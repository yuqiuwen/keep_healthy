from django.urls import path
from .views import DiabetesViewSet as diabetes

urlpatterns = [
    path(r'fetch_diabetes_data/', diabetes.as_view({'get': 'fetch_diabetes_data'})),
    path(r'start_pred_diabetes/', diabetes.as_view({'post': 'start_pred_diabetes'})),

]