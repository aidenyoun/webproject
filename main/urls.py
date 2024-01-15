from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('save_medication/<int:medication_id>/', views.save_medication, name='save_medication'),
    path('get_medications/', views.get_medications, name='get_medications'),
]
