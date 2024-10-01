from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('about', views.about, name='about'),
    path('student/', views.student_index, name='student_index'),
    path('student/create/', views.student_create, name='student_create'),
]