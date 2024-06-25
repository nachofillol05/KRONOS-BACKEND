from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    verify_email,
    RegisterView,
    OlvideMiContrasenia,
    change_password,
    ProfileView,
    TeacherListView,
    TeacherDetailView,
    ExcelToteacher,
    DniComprobation,
    SubjectListCreate, 
    SubjectRetrieveUpdateDestroy,
    ModuleViewSet,
    verifyToken,
    SchoolsView,
    CourseListCreate, 
    CourseRetrieveUpdateDestroy,
    YearListCreate,
    YearRetrieveUpdateDestroy,
    PreceptorsView
)


router = DefaultRouter()
router.register(r'modules', ModuleViewSet)


urlpatterns = [
    # Users
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uuid:token>/', verify_email, name='verify-email'),
    path('Register/', RegisterView.as_view(), name='register'),
    path('ForgotPassword/', OlvideMiContrasenia.as_view(), name='OlvideMiContrasenia'),
    path('forgot-password/<uuid:token>/', change_password, name='forgot-password'),
    path('profile', ProfileView.as_view(), name='profile'),
    # Schools
    path('user_schools/', SchoolsView.as_view(), name='user_schools'),
    path('schools/<int:pk>/preceptors', PreceptorsView.as_view(), name='preceptors'),
    # Subject
    path('subjects/', SubjectListCreate.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroy.as_view(), name='subject-detail'),
    # courses
    path('courses/', CourseListCreate.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroy.as_view(), name='course-detail'),
    # Year
    path('years/', YearListCreate.as_view(), name='year-list-create'),
    path('years/<int:pk>/', YearRetrieveUpdateDestroy.as_view(), name='year-detail'),
    # Teachers
    path('teachers/', TeacherListView.as_view(), name='get_teachers'),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), name='detail_teacher'),
    path('create_teacher/', DniComprobation.as_view(), name='Comprobation_DNI'),
    path('teacher_word/', ExcelToteacher.as_view(), name='teacher_word'),
    
    path('verifyToken/', verifyToken.as_view(), name='verifyToken'),
]

urlpatterns += router.urls
