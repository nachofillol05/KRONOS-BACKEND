from django.urls import path
from .views import LoginView, verify_email,RegisterView, SchoolListView, SchoolCreateView, SubjectListCreate, SubjectRetrieveUpdateDestroy

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uuid:token>/', verify_email, name='verify-email'),
    path('Register/', RegisterView.as_view(), name='register'),
    path('schools/', SchoolListView.as_view(), name='get_schools'),
    path('create_schools/', SchoolCreateView.as_view(), name='create_school'),
    path('subjects/', SubjectListCreate.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroy.as_view(), name='subject-detail')
]