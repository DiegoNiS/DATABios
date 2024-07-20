# Proyecto/inventario/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('listar_pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('crearpedidos/', views.crear_pedidos, name='crear_pedidos'),
    path('listar_proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('crear_proveedores/', views.crear_proveedores, name='crear_proveedores'),
]
