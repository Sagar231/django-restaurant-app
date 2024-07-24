
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.index, name="index"),
    path('login/',views.userlogin ,name = 'login'),
    path('logout/',views.userlogout,name='logout'),
    path('register/',views.register,name='register'),
]