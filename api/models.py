import uuid # Para usar ids UUID
from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Jugador(models.Model): # Modelo jugador
    # Esto genera un selector de opciones
    MANO_CHOICES = [
        ("D", "Diestra"),
        ("Z", "Zurda"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Identidad
    nombre_completo = models.CharField(max_length=150)
    pais = models.CharField(max_length=50)
    bandera = models.CharField(max_length=5, blank=True, null=True) # Codigo ISO
    fecha_nacimiento = models.DateField(blank=True, null=True)

    # Datos deportivos
    ranking_atp = models.IntegerField(blank=True, null=True)
    mejor_ranking = models.IntegerField(blank=True, null=True)
    mano_dominante = models.CharField(max_length=1, choices=MANO_CHOICES)

    # Multimedia
    foto = models.ImageField(upload_to="jugadores/", blank=True, null=True)

    # Info

    creacion = models.DateTimeField(auto_now_add=True)
    actualizacion = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nombre_completo
    
class Partido(models.Model): # Modelo partido

    # Estado del partido para validaciones
    ESTADO_CHOICE = [
        ("pen", "Pendiente"),
        ("gam", "En Juego"),
        ("fin", "Finalizado"),
    ]

    FASE_CHOICE = [
        ("1", "Final"),
        ("2", "Semi-final"),
        ("3", "Cuartos de final"),
        ("4", "Octavos de final"),
        ("5", "Dieciseisavos de final"),
        ("6", "2ª Ronda"),
        ("7", "1ª Ronda"),
        ("8", "Fase Previa"),
        ("0", "Amistoso"),
    ]


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Información del partido
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICE, default="pen")
    competicion = models.CharField(max_length=200)
    fase = models.CharField(max_length=1, choices=FASE_CHOICE, default="0")
    annio = models.PositiveIntegerField()
    fecha_iniciado = models.DateTimeField(null=True, blank=True)
    fecha_finalizado = models.DateTimeField(null=True, blank=True)

    #Estado del partido
    is_tie_break = models.BooleanField(default=False)

    # Una vez haya empezado el partido solo el arbitro o un admin pueden modificarlo
    arbitro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="partidos_arbitrados"
    )

    ganador = models.ForeignKey(
        "Jugador",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="partidos_ganados"
    )

    # Info del sistema
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.competicion} - {self.fase}"
    
    def iniciar_partido(self, arbitro):
        if self.estado!="pen":
            raise ValueError("El partido ya ha sido iniciado.")
        
        self.estado = "gam"
        self.arbitro = arbitro
        self.fecha_inicio = timezone.now()
        self.save()
    
    def finalizar_partido(self, ganador):
        if self.estado != "gam":
            raise ValueError("El Partido no esta en juego")
    
        if ganador is None:
            raise ValueError("Debe existir un ganador para finalizar el partido")

        self.estado = "fin"
        self.ganador = ganador
        self.fecha_finalizado = timezone.now()
        self.save()
    
class PartidoParticipante(models.Model): # Modelo de jugadores de un patido
    partido = models.ForeignKey(
        Partido,
        related_name = "participantes",
        on_delete=models.CASCADE
    )

    jugador = models.ForeignKey(
        "Jugador",
        on_delete=models.CASCADE
    )

    es_jugador1 = models.BooleanField(default=True)

    sets_1 = models.PositiveIntegerField(default=0)
    sets_2 = models.PositiveIntegerField(default=0)
    sets_3 = models.PositiveIntegerField(default=0)

    saque = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.jugador} ({'Jug1' if self.es_jugador1 else 'Jug2'})"
    
    