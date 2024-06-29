# Proyecto/inventario/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/filtrar/', views.filtrar_productos, name='filtrar_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/detalle/<int:pk>', views.detalle_producto, name='detalle_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:pk>/edit/', views.modificar_categoria, name='modificar_categoria'),
    path('categorias/<int:pk>/delete/', views.eliminar_categoria, name='eliminar_categoria'),

]
