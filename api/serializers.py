from rest_framework import serializers # Paquete validar y transformar en json una consuta
from .models import Jugador, PartidoParticipante, Partido
from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_username(self, value):
        if User.objects.filter(username=value).exists:
            raise serializers.ValidationError("Este usuario ya existe")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya esta registrado")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        return user

class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields ="__all__" # <- Con esto indicamos que queremos todos los datos del modelo en la BBDD

class ParticipantePartidoSerializer(serializers.ModelSerializer):
    # Campo calculado que viene de una relación con el modelo Jugador
    jugador_nombre = serializers.CharField(source="jugador.nombre_completo",read_only=True)

    class Meta:
        model = PartidoParticipante
        fields = ("jugador", "jugador_nombre", "es_jugador1", "sets_1", "sets_2", "sets_3", "saque") # <- Con esto indicamos que queremos todos los datos del modelo en la BBDD

class PartidoSerializer(serializers.ModelSerializer):
    # Esta linea sirve para indicar una relación N:M entre Partidos y Jugadores
    participantes = ParticipantePartidoSerializer(many=True, read_only=True)

    class Meta:
        model = Partido
        fields = "__all__" # <- Con esto indicamos que queremos todos los datos del modelo en la BBDD
        read_only_fields = [ #Blindamos datos que no se deben modificar facimente
            "estado", "arbitro", "fecha_inicio", "fecha_finalizado", "ganador"
        ]
    
    def validate(self, data):
        instance = self.instance

        if instance:
            #Validacion del tie break
            nuevo_tie_break = data.get("is_tie_break", instance.is_tie_break)
            if instance.estado != "gam" and nuevo_tie_break != instance.is_tie_break:
                raise serializers.ValidationError({
                    "is_tie_break" : "No se puede modificar antes de empezar el partido"
                })
            # Si ya existe un ganador, no se debe de poder modificar
            if "ganador" in data and data["ganador"] != instance.ganador:
                raise serializers.ValidationError(
                    {"ganador" : "No se puede modificar al ganador del partido manualmente"}
                )    
        return data