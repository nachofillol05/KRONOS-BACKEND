from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = 
    path('admin/', admin.site.urls, name="admin_site"),
    path('api/', include('Kronosapp.urls')),
    # yaml UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # docs
    path('api/doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
