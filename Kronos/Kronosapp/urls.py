from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    RegisterView,
    OlvideMiContrasenia,
    reset_password,
    ChangePasswordView,
    ProfileView,
    TeacherListView,
    ExcelToteacher,
    DniComprobation,
    SubjectListCreate, 
    SubjectRetrieveUpdateDestroy,
    ModuleViewSet,
    verifyToken,
    TeacherSchoolsView,
    CourseListCreate, 
    CourseRetrieveUpdateDestroy,
    YearListCreate,
    YearRetrieveUpdateDestroy,
    PreceptorsView,
    Newscheduleview,
    NewScheduleCreation,
    EventListCreate,
    EventRetrieveUpdateDestroy,
    EventTypeViewSet,
    DocumentTypeViewSet,
    ContactarPersonal,
    DirectiveSchoolsView
)
from .utils import (
    verify_email
)


router = DefaultRouter()
router.register(r'modules', ModuleViewSet)


urlpatterns = [
    # Users
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uuid:token>/', verify_email, name='verify-email'),
    path('Register/', RegisterView.as_view(), name='register'),
    path('forgotPassword/', OlvideMiContrasenia.as_view(), name='OlvideMiContrasenia'),
    path('forgot-password/<uuid:token>/', reset_password, name='forgot-password'),
    path('changePassword/', ChangePasswordView.as_view(), name='ChangePassword'),
    
    # Schools
    path('user_schools/', TeacherSchoolsView.as_view(), name='user_schools'),
    path('preceptors/', PreceptorsView.as_view(), name='preceptors'),
    path('directive_schools/', DirectiveSchoolsView.as_view(), name='directive_schools'),
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
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create_teacher/', DniComprobation.as_view(), name='Comprobation_DNI'),
    path('teacher_word/', ExcelToteacher.as_view(), name='teacher_word'),
    # Event
    path('events/', EventListCreate.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroy.as_view(), name='event-detail'),
    # EventType
    path('typeevent/', EventTypeViewSet.as_view(), name='eventType-list-create'),
    #DocumentType
    path('documentTypes/', DocumentTypeViewSet.as_view(), name='document-type-list-create'),
    # Verify Token

    path('contacting-staff/', ContactarPersonal.as_view(), name='contacting-staff'),
    
    path('verifyToken/', verifyToken.as_view(), name='verifyToken'),

    path('new_schedule/', Newscheduleview.as_view(), name='create_schedule'),
    path('create_schedule/', NewScheduleCreation.as_view(), name='create_schedule')

]

urlpatterns += router.urls
