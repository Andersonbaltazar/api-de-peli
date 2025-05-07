from django.db import models

class Genero(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Director(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return self.nombre

class Actor(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return self.nombre

class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    año = models.IntegerField()
    sinopsis = models.TextField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    generos = models.ManyToManyField(Genero)
    actores = models.ManyToManyField(Actor, through='Reparto') # Usamos 'Reparto' como tabla intermedia

    def __str__(self):
        return self.titulo

class Reparto(models.Model):  #Tabla intermedia
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    personaje = models.CharField(max_length=100)

class Calificacion(models.Model): #para calificar peliculas
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='calificaciones')
    usuario = models.CharField(max_length=100)  # Podrías usar User de Django
    calificacion = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    reseña = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('pelicula', 'usuario')  # Un usuario solo puede calificar una película una vez