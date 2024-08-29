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
    SchoolsView,
    CourseListCreate, 
    CourseRetrieveUpdateDestroy,
    YearListCreate,
    YearRetrieveUpdateDestroy,
    PreceptorsView,
    Newscheduleview,
    NewScheduleCreation,
    EventListCreate,
    EventRetrieveUpdateDestroy,
    AffiliatedView,
    EventTypeViewSet,
    DocumentTypeViewSet,
    TeacherSubjectSchoolListCreateView,
    TeacherSubjectSchoolDetailView,
    TeacherAvailabilityListCreateView,
    TeacherAvailabilityDetailView,
    SubjectPerModuleView,
    RoleView,
    UserRolesViewSet,
    SchoolStaffAPIView,
    DirectivesView,
    ContactarPersonal,
    ViewSchedule,
    StaffToExel
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
    path('user_schools/', SchoolsView.as_view(), name='user_schools'),
    path('preceptors/', PreceptorsView.as_view(), name='preceptors'),
    path('directives/', DirectivesView.as_view(), name='directives'),
    # Subject
    path('subjects/', SubjectListCreate.as_view(), name='subject-list-create'),
    path('subjects/?export=excel', SubjectListCreate.as_view(), name='subject-list-create-excel'),
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
    path('events/affiliated/', AffiliatedView.as_view(), name='event-affiliated'),
    # EventType
    path('typeevent/', EventTypeViewSet.as_view(), name='eventType-list-create'),
    #DocumentType
    path('documentTypes/', DocumentTypeViewSet.as_view(), name='document-type-list-create'),
    #roles
    path('roles/', RoleView.as_view(), name='role-list-create'),
    
    #teacher_subject_school
    path('teachersubjectschool/', TeacherSubjectSchoolListCreateView.as_view(), name='teachersubjectschool-list-create'),
    path('teachersubjectschool/<int:pk>/', TeacherSubjectSchoolDetailView.as_view(), name='teachersubjectschool-detail'),
    #teacherAvailability
    path('teacheravailability/', TeacherAvailabilityListCreateView.as_view(), name='teacher-availability-list-create'),
    path('teacheravailability/<int:pk>/', TeacherAvailabilityDetailView.as_view(), name='teacher-availability-detail'),
    #Myroles
    path('school/myroles/', UserRolesViewSet.as_view(), name='user-roles'),
    #SchoolStaff
    path('staff/', SchoolStaffAPIView.as_view(), name='school-staff'),
    path('staff/export', StaffToExel.as_view(), name='school-staff-excel'),
    # Verify Token

    path('contacting-staff/', ContactarPersonal.as_view(), name='contacting-staff'),
    
    path('verifyToken/', verifyToken.as_view(), name='verifyToken'),

    # Schedule
    path('new_schedule/', Newscheduleview.as_view(), name='create_schedule'),
    path('create_schedule/', NewScheduleCreation.as_view(), name='create_schedule'),
    path('subjectpermodule/', SubjectPerModuleView.as_view(), name='subjectpermodule'),
    path('viewschedule/', ViewSchedule.as_view(), name='viewschedule')
    


]

urlpatterns += router.urls
