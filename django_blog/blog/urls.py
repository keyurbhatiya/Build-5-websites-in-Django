from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('newpost/', views.newPost, name='newPost'),
    path('mypost/', views.myPost, name='myPost'),
    path('signout/', views.signout, name='signout'),
]