from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    verify_email,
    RegisterView,
    OlvideMiContrasenia,
    change_password,
    ProfileView,
    SchoolsView,
    SchoolView,
    TeacherListView,
    TeacherDetailView,
    ExcelToteacher,
    DniComprobation,
    SubjectListCreate, 
    SubjectRetrieveUpdateDestroy,
    ModuleViewSet,
    PreceptorListCreateView,
    verifyToken
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
    path('schools/', SchoolsView.as_view(), name='schools'),
    path('schools/<int:pk>', SchoolView.as_view(), name='school'),
    path('schools/<int:pk>/preceptors', PreceptorListCreateView.as_view(), name='preceptors'),
    # Subject
    path('subjects/', SubjectListCreate.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroy.as_view(), name='subject-detail'),
    # Teachers
    path('teachers/', TeacherListView.as_view(), name='get_teachers'),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), name='detail_teacher'),
    path('create_teacher/', DniComprobation.as_view(), name='Comprobation_DNI'),
    path('teacher_word/', ExcelToteacher.as_view(), name='teacher_word'),
    
    path('verifyToken/', verifyToken.as_view(), name='verifyToken'),
]

urlpatterns += router.urls
