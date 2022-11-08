from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'auth'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('check/token/<str:token>/', views.check_token, name='check_token'),
    path('token/', obtain_auth_token, name='api_token_auth'),
]
