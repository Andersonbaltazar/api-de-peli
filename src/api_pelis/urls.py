from django.urls import path, include
from rest_framework import routers
from .views import PeliculaViewSet, DirectorViewSet, ActorViewSet, CalificacionViewSet

router = routers.DefaultRouter()
router.register(r'peliculas', PeliculaViewSet)
router.register(r'directores', DirectorViewSet)
router.register(r'actores', ActorViewSet)
router.register(r'calificaciones', CalificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]