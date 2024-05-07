from django.urls import path
from .views import LoginView, verify_email,RegisterView, SchoolListView, SchoolCreateView,OlvideMiContrasenia,change_password

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uuid:token>/', verify_email, name='verify-email'),
    path('Register/', RegisterView.as_view(), name='register'),
    path('schools/', SchoolListView.as_view(), name='get_schools'),
    path('create_schools/', SchoolCreateView.as_view(), name='create_school'),
    path('ForgotPassword/', OlvideMiContrasenia.as_view(), name='OlvideMiContrasenia'),
    path('forgot-password/<uuid:token>/', change_password, name='forgot-password')
]