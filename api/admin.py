from django.contrib import admin
from .models import Jugador, Partido, PartidoParticipante
# Importaciones de los metodos para trabajar con CSV
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class JugadorResource (resources.ModelResource):
    class Meta:
        model = Jugador

        skip_unchanged = True
        report_skipped = True

@admin.register(Jugador)
class JugadorAdmin(ImportExportModelAdmin): # Registra el modelo Jugador en la pagina de admin
    resource_class = JugadorResource
    list_display = ("nombre_completo", "pais", "ranking_atp") # Columnas visibles en el resumen de la pagina Admin
    search_fields = ("nombre_completo", "pais") # Campos para poder hacer busquedas

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

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ("competicion", "fase", "annio")
    search_fields = ("competicion", "fase", "annio")