"""
Definition of urls for Realtimeobjectdetection.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('Sign_in', views.Sign_in, name='Sign_in'),
    path('home/', views.home, name='home'),
    path('camera_site/', views.camera_site, name ='camera_site'),
    path('about/', views.about, name = 'about'),
    path('video_feed', views.video_feed, name= "video_feed"),
    path('about/', views.about, name='about'),
    path('service/', views.service, name= 'service'),
    path('contact/', views.contact, name= 'contact'),
    path('sign_in_form/', views.sign_in_form, name = 'sign_in_form'),
    path('logout_user/', views.logout_user, name = 'logout_user'),
]
