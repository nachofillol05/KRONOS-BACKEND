from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verifyToken', TokenVerifyView.as_view(), name='verify_token'),
    path('api/', include('Kronosapp.urls')),
    # yaml UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # docs
    path('api/doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
