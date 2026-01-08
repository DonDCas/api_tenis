"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # Habilita panel de Admin
from django.urls import path, include # Metodos para añadir rutas URL
from django.conf import settings
from django.conf.urls.static import static # Permite usar archivos multimedia
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # Función para optener un token
    TokenRefreshView,   # Función para refrescar un token
)
from drf_spectacular.views import (
    SpectacularAPIView,     # Generador de swagger
    SpectacularSwaggerView, # Muestra la documentación
)
from api.views import UserRegisterView

urlpatterns = [
    # Ruta para acceder al panel de admin
    path('admin/', admin.site.urls),

    # ruta para obtener token
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Ruta para refrescar el token
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Ruta para acceder a la documentación de Swagger
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),

    # Recibe las rutas de la api
    path("api/v1/", include("api.urls")),
    
    path("api/register/", UserRegisterView.as_view(), name='user-register')
]

# Para permitir a usuarios subir archivos multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)