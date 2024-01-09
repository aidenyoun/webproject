from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum, name='forum'),
    path('new/', views.post_new, name='post_new'),
    path('posts/', views.post_view, name='post_view'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<str:category>', views.forum, name='forum_category'),
]