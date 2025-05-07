from rest_framework import serializers
from .models import Pelicula, Director, Actor, Reparto, Genero, Calificacion

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class RepartoSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()  # Incluimos los detalles del actor
    class Meta:
        model = Reparto
        fields = ['actor', 'personaje']

class PeliculaSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()  # Incluimos los detalles del director
    generos = GeneroSerializer(many=True)
    actores = RepartoSerializer(many=True, source='reparto_set') # Usamos el related_name
    calificaciones = serializers.SerializerMethodField()

    class Meta:
        model = Pelicula
        fields = ['id', 'titulo', 'año', 'sinopsis', 'director', 'generos', 'actores', 'calificaciones']

    def get_calificaciones(self, obj):
      # Calcula el promedio y la cantidad de calificaciones
        calificaciones = obj.calificaciones.all()
        total_calificaciones = calificaciones.count()
        suma_calificaciones = sum(c.calificacion for c in calificaciones)
        promedio_calificacion = suma_calificaciones / total_calificaciones if total_calificaciones > 0 else 0
        return {
            'promedio': promedio_calificacion,
            'total': total_calificaciones
        }
class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['id', 'usuario', 'calificacion', 'reseña']