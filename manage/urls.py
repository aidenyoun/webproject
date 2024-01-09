from django.urls import path
from . import views

app_name = 'manage'

urlpatterns = [
    path('', views.manage, name='manage'),
]