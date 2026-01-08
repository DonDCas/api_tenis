from django.contrib import admin
from .models import Jugador, Partido, PartidoParticipante

# Register your models here.


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin): # Registra el modelo Jugador en la pagina de admin
    list_display = ("nombre_completo", "pais", "ranking_atp") # Columnas visibles en el resumen de la pagina Admin
    search_fields = ("nombre_completo", "pais") # Campos para poder hacer busquedas

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ("competicion", "fase", "annio")
    search_fields = ("competicion", "fase", "annio")

@admin.register(PartidoParticipante)
class ParticipantePartidoAdmin(admin.ModelAdmin):
    list_display = ("jugador_nombre", "partido_competicion", "partido_fase", "es_jugador1")

    def jugador_nombre(self, obj):
        return obj.jugador.nombre_completo
    jugador_nombre.admin_order_field = "jugador__nombre_completo"
    jugador_nombre.short_description = "Jugador"

    def partido_competicion(self, obj):
        return obj.partido.competicion
    partido_competicion.admin_order_field = "partido__competicion"
    partido_competicion.short_description = "Competición"

    def partido_fase(self, obj):
        return obj.partido.fase
    partido_fase.admin_order_field = "partido__fase"
    partido_fase.short_description = "Fase"

