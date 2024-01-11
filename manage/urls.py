from django.urls import path
from . import views

app_name = 'manage'

urlpatterns = [
    path('', views.manage, name='manage'),
    path('calendar/', views.calendar, name='calendar'),
    path('manage_medicine/', views.manage_medicine, name='manage_medicine'),
    path('edit_medicine/', views.edit_medicine, name='edit_medicine'),
    path('delete_medicine/', views.delete_medicine, name='delete_medicine'),
]