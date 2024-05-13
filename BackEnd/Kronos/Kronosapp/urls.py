from django.urls import path
from .views import (
    LoginView,
    verify_email,
    RegisterView,
    OlvideMiContrasenia,
    change_password,
    SchoolListView,
    SchoolCreateView,
    SchoolDetailView,
    TeacherListView,
    TeacherDetailView
)


urlpatterns = [
    # Users
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uuid:token>/', verify_email, name='verify-email'),
    path('Register/', RegisterView.as_view(), name='register'),
    path('ForgotPassword/', OlvideMiContrasenia.as_view(), name='OlvideMiContrasenia'),
    path('forgot-password/<uuid:token>/', change_password, name='forgot-password'),
    # Schools
    path('schools/', SchoolListView.as_view(), name='get_schools'),
    path('create_schools/', SchoolCreateView.as_view(), name='create_school'),
    path('school/<int:pk>', SchoolDetailView.as_view(), name='create_school'),
    # Teachers
    path('teachers/', TeacherListView.as_view(), name='get_teachers'),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), name='create_teacher'),
]