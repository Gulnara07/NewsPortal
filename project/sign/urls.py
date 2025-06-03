from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, upgrade_me
from . import views

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='flatpages/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='flatpages/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='flatpages/signup.html'),
         name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

]
