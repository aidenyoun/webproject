from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('save_medication/', views.save_medication, name='save_medication'),
]
