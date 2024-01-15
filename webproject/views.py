from django.contrib import admin
from django.urls import include, path
from board.views import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path
    path('board/', include('board.urls')),
    path('common/', include('common.urls')),
    path('search/', include('search.urls')),
    path('manage/', include('manage.urls')),
    path('forum/', include('forum.urls')),
]
