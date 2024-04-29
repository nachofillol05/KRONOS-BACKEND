from django.urls import path
from .views import LoginView, verify_email,RegisterView

urlpatterns = [
    
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uuid:token>/', verify_email, name='verify-email'),
    path('Register/', RegisterView.as_view(), name='register'),
]