from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('api/login/', views.LoginView.as_view(), name='api_login'),
    path('api/verify-token/', views.VerifyTokenView.as_view(), name='api_verify_token'),
]
