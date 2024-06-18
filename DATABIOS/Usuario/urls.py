from django.urls import path
from .views import loginView, homeView, logout, list_usuarios

urlpatterns = [
    path('', loginView, name='login'),  # Login es la primera ruta
    path('usuarios', list_usuarios, name='lista_usuarios'),
    path('home/', homeView, name='home'), # Max's Creations
    path('logout/', logout, name='logout'),
]
