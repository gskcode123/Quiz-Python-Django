from django.urls import path
from . import views
urlpatterns = [
    path('quiz/', views.quiz,name="blog-quiz"),
    path('', views.home,name="blog-home"),
    path('progress/', views.progress,name="blog-progress"),
    path('start/',views.start,name='start'),
    path('next/',views.nextQuestion,name='next'),
]
