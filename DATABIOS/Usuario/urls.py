from django.urls import path
from .views import loginView, homeView, logout, list_usuarios, agregar_usuario, inicio_sesion, cerrar_sesion, eliminar_usuario

urlpatterns = [
    path('', inicio_sesion, name='login'),
    path('usuarios/', list_usuarios, name='lista_usuarios'),
    path('agregar/', agregar_usuario, name='agregar_usuario'),
    path('eliminar/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('logout/', cerrar_sesion, name='logout'),
    path('home/', homeView, name='home'), # Max's Creations
    path('max', loginView, name='loginM'),  # Login es la primera ruta
    path('logout/', logout, name='logoutM'),
]

