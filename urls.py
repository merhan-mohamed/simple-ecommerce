from django.urls import path
from . import views
from .views import signup

app_name ='accounts'
urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile/<slug:slug>', views.profile, name='profile'),
]