from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum, name='forum'),
    path('posts/', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<str:category>', views.forum, name='forum_category'),
    path('comment_new/<int:pk>/', views.comment_new, name='comment_new'),
    path('comment_edit/<int:pk>/', views.comment_edit, name='comment_edit'),
    path('posts/<int:pk>/recommend', views.recommend_post, name='recommend_post'),
    path('comment_delete/<int:pk>/', views.comment_delete, name='comment_delete'),
    path('comment/<int:pk>/recommend/', views.recommend_comment, name='recommend_comment'),
]