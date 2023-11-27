from django.urls import path
from . import views
urlpatterns = [

    # pages-name,action of that  page,name=default

    # path('', views.login, name="login"),
    path('login', views.login, name="login"),
    path('registration', views.registration, name="registration"),
    path('' ,views.homepage ,name='homepage'),


    path('user_home', views.user_home, name="user_home"),
    path('logout', views.logout, name="logout"),
    path('adminhome', views.adminhome , name="adminhome"),
    path('addboats', views.addboat, name="addboat"),
    path('profile', views.profile, name='profile'),
    path('updateprofile', views.updateprofile, name='updateprofile'),
    path('viewboats', views.viewboats, name='viewboats'),
    path('updateboat/<int:boat_id>',views.updateboats, name='updateboats'),
    path('deleteboat/<int:boat_id>/', views.deleteboat),
    path('Contactus', views.about, name='about'),
    path('userboat', views.userboat, name='userboat'),




]
