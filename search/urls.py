from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'search'

urlpatterns = [
    path('', views.search, name='search'),
    path('name_search/', views.name_search, name='name_search'),
    path('pic_search/', views.PicSearchView.as_view(), name='pic_search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
