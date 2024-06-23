# Proyecto/inventario/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/edit/', views.modificar_producto, name='modificar_producto'),
    path('productos/<int:pk>/delete/', views.eliminar_producto, name='eliminar_producto'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:pk>/edit/', views.modificar_categoria, name='modificar_categoria'),
    path('categorias/<int:pk>/delete/', views.eliminar_categoria, name='eliminar_categoria'),

]
