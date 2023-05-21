from django.contrib import admin
from django.urls import path, include
from quiz import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.loginuser, name='login'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    path('quizselect', views.quizselect, name='quizselect'),
    path('quizpage', views.quizpage, name='quizpage'),
    path('score', views.score, name='score'),
    path('base', views.index, name='invalid-request'),
    path('signupuser', views.signupuser, name='signupuser'),
    path('api/get-quiz/', views.get_quiz, name='get-quiz')
]
