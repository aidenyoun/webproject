from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)