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
from api.views import UserRegisterView, UserMeView

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
    
    path("api/register/", UserRegisterView.as_view(), name='user-register'),
    path('api/v1/user/me/', UserMeView.as_view(), name='user-me')
]

# Para permitir a usuarios subir archivos multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)