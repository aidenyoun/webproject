from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('board/', include('board.urls')),
    path('common/', include('common.urls')),
    path('search/', include('search.urls')),
    path('manage/', include('manage.urls')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('api/', include('forum.urls', namespace='api')),
    path('mypage/', include('mypage.urls')),

    path('', include('main.urls')),
]
