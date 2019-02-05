from django.urls import path
#from accounts.views import login_view, logout_view
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('login/', auth_views.login, name='login' ),
    path('logout/', auth_views.logout, name='logout'),
    path('add_new_church', views.add_new_church, name='add_new_church'),
    #path('forget_password/', include('accounts.urls')),
]
