from rest_framework import viewsets, generics, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pelicula, Director, Actor, Calificacion
from .serializers import PeliculaSerializer, DirectorSerializer, ActorSerializer, CalificacionSerializer
from django_filters.rest_framework import DjangoFilterBackend

class PeliculaViewSet(viewsets.ModelViewSet):
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['año', 'director__nombre', 'generos__nombre']  # Filtro por año, director y género
    search_fields = ['titulo', 'sinopsis']  # Búsqueda por título y sinopsis

    @action(detail=True, methods=['POST'])
    def agregar_a_favoritos(self, request, pk=None):
        pelicula = self.get_object()
        # Aquí iría la lógica para agregar a favoritos (requiere autenticación y un modelo de Usuario)
        # Por simplicidad, lo dejaremos como un ejemplo
        return Response({'status': 'Agregado a favoritos'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def ver_favoritos(self, request, pk=None):
      # Aquí iría la lógica para ver peliculas favoritas del usuario
      return Response([], status=status.HTTP_200_OK)

class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pelicula_id = serializer.validated_data['pelicula'].id
        usuario = serializer.validated_data['usuario'] # Aquí deberías obtener el usuario autenticado
        try:
            Calificacion.objects.get(pelicula_id=pelicula_id, usuario=usuario)
            return Response({'detail': 'Ya has calificado esta película.'}, status=status.HTTP_400_BAD_REQUEST)
        except Calificacion.DoesNotExist:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
