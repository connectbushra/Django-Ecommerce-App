from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include
from . import views
# from .views import ResetPasswordEmailApiView,PasswordTokenCheckApi
app_name='account'

urlpatterns = [
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("logout", views.logout, name="logout"),
    path("change_password/<token>/",views.Reset_password,name="change_password"),
    path('forget_password/',views.forget_password,name="forget_password"),
]