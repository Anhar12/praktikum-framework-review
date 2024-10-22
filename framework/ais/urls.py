from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter
from .views import StudentsViewSet

router = DefaultRouter()
router.register(r'students', StudentsViewSet)

urlpatterns = [
    path('', views.homepage, name='home'),
    path('about', views.about, name='about'),
    path('student/', views.student_index, name='student_index'),
    path('student/create/', views.student_create, name='student_create'),
    path('student/update/<int:student_id>/', views.student_update, name='student_update'),
    path('student/delete/<int:student_id>', views.student_delete, name='student_delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/student', views.dashboard_student, name='dashboard_student'),
    path('dashboard/teacher', views.dashboard_teacher, name='dashboard_teacher'),
    path('api/', include(router.urls)),
]