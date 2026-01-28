from django.shortcuts import render # import estandar de django esta por si acaso
from rest_framework.viewsets import ModelViewSet  # Esto sirve para proporcionar de forma automatica todos los verbos
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action # permite crear enpoints personalizados
from rest_framework.response import Response # Permite enviar respuesta HTTP al cliente
from rest_framework import status, generics # Permite usar los codigo para informar de lo que esta pasando al usuario
from .models import Jugador, Partido, PartidoParticipante #Modelos ya creados
from .serializers import JugadorSerializer, PartidoSerializer, ParticipantePartidoSerializer, UserRegisterSerializer # Paquete para serializar en JSON
from django.contrib.auth.models import User
from .permissions import IsAuthenticatedOrReadOnlyGet # Para dar permisos de solo lectura
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model



User = get_user_model()
# Cr0eate your views here.

# En estas clases se generan automaticamente todos los ENDPOINT
class JugadorViewSet(ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    #permission_classes = [AllowAny] # <- Borrar despues
    permission_classes = [IsAuthenticatedOrReadOnlyGet]

class PartidoViewSet(ModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyGet]

    @action(detail=True, methods=["post"])
    def iniciar(self, request, pk=None):
        partido = self.get_object()

        if not partido.participantes.exists():
            return Response(
                {"error": "No se puede iniciar un partido sin jugadores"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            #Suponemos que el usuario es el arbitro del partido
            partido.iniciar_partido(arbitro=request.user) # Iniciamos el partido mediante la función del modelo
        except ValueError as e:
            return Response({"error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(partido)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        partido = self.get_object()

        if not request.user.is_superuser and request.user != partido.arbitro:
            return Response({"error": "No tienes permiso para finalizar este partido"}, status=403)

        # Este dato viene en el body que nos mande la app
        ganador_id = request.data.get("ganador_id")
        if not ganador_id:  # Si no viene el id del ganador devolvemos un error
            return Response(
                {"error" : "Error, hay que especificar un ganador"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
             # Comprobamos si el id del jugador es de alguno de los jugadores de este partido
        if not partido.participantes.filter(jugador__id=ganador_id).exists():
            return Response(
                {"error": "El jugador indicado no pertenece al partido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ganador = get_object_or_404(Jugador, id=ganador_id)
        
        try:
            partido.finalizar_partido(ganador) # Finalizamos el partido mediante la función del modelo
        except ValueError as e:
            return Response(
                {"Error" : str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(partido)
        return Response(serializer.data, status = status.HTTP_200_OK)

class ParticipantePartidoViewSet(ModelViewSet):
    queryset = PartidoParticipante.objects.all()
    serializer_class = ParticipantePartidoSerializer

    @action(detail=True, methods=["post"], url_path="add-jugador")
    def add_jugador(self, request, pk=None):
        partido = self.get_object()
        jugador_id = request.data.get("jugador_id")

        if not request.user.is_superuser and request.user != partido.arbitro:
            return Response(
                {"error": "No tienes permiso para modificar este partido"},
                status = status.HTTP_403_FORBIDDEN
            )

        if (partido.estado != "pen"):
            return Response(
                {"error" : "No se pueden modificar los jugadores una vez iniciado el partido"},
                status = status.HTTP_400_BAD_REQUEST
            )

        if partido.participantes.count() >= 2:
            return Response(
                {"error" : "Ya estan todos los jugadores seleccionados"},
                status = status.HTTP_400_BAD_REQUEST
            )

        if not jugador_id: # Comprobamos que en el body venga una ID de jugador
            return Response(
                {"error" : "Se debe de indicar la id de un jugador"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        jugador = get_object_or_404(Jugador, id = jugador_id)
        
        if partido.participantes.filter(jugador = jugador).exists():
            return Response(
                {"error" : "El jugador indicado ya existe en el partido"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        PartidoParticipante.objects.create(
            partido = partido,
            jugador = jugador
        )

        return Response(
            {"mensaje" : "Jugador añadido correctamente"},
            status = status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=["post"], url_path="remove-jugador")
    def remove_jugador(self, request, pk=None):
        partido = self.get_object()
        jugador_id = request.data.get("jugador_id")

        if not request.user.is_superuser and request.user != partido.arbitro:
            return Response(
                {"error": "No tienes permiso para modificar este partido"},
                status = status.HTTP_403_FORBIDDEN
            )

        if not jugador_id:
            return Response(
                {"error" : "No se ha indicado el id del jugador"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        # Comprobamos que el partido no haya comenzado y que si no es un superusuario no se pueda modificar en caso de que el partido ya haya empezado
        if partido.estado != "pen":
            return Response(
                {"error" : "No pueden modificar los jugadores una vez empezado el partido"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        # Impedimos borrar cuando haya 2 o más jugadores salvo que se sea super usuario
        if partido.participantes.count() <= 2:
            return Response(
                {"error": "Un partido debe tener al menos dos jugadores"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        participante = partido.participantes.filter(jugador__id = jugador_id).first()

        if not participante:
            return Response(
                {"error" : "El jugador elegido no participa en este partido"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        participante.delete()

        return Response(
            {"mensaje" : "Se confirma la eliminación del participante del partido"},
            status = status.HTTP_200_OK
        )
    
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    