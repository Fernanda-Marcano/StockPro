from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.SignUpView.as_view(), name='registrarse'),
    path('logout/', views.custom_logout, name='custom-logout'),
    path('update-profile/', views.UserProfileUpdateView.as_view(), name='update-profile'),
]