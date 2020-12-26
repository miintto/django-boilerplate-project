from django.urls import path
from app_test import views


urlpatterns = [
    path('sample', views.TestSampleView.as_view())
]
