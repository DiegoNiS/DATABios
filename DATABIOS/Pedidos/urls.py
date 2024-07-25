from django.urls import path
from . import views


urlpatterns = [
    path('listar_pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('crear_pedidos/', views.crear_pedidos, name='crear_pedidos'),
    #path('listar_proveedores/', views.listar_proveedores, name='listar_proveedores'),
    #path('crear_proveedores/', views.crear_proveedores, name='crear_proveedores'),
]
