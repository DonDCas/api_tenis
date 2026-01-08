from rest_framework.routers import DefaultRouter # Genera el CRUD automaticamente
from .views import JugadorViewSet, PartidoViewSet, ParticipantePartidoViewSet # Importa las clases del modulo views

router = DefaultRouter() # Sirve para crear urls basadas en los ViewSets
# Con register registramos el modelo del que queremos generar las rutas
router.register(r"jugadores", JugadorViewSet, basename="jugador") #con basename generamos otra ruta personalizada
router.register(r"partidos", PartidoViewSet)
router.register(r"participantes", ParticipantePartidoViewSet)

urlpatterns = router.urls