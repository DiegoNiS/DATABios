# ventas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ventas_list, name='ventas_list'),
    path('detalle/<int:venta_id>/', views.venta_detail, name='venta_detail'),
    path('agregar/', views.agregar_venta, name='agregar_venta'),
    path('agregar_producto/', views.agregar_producto_venta, name='agregar_producto_venta'),
    path('eliminar_producto/<int:detalle_id>/', views.eliminar_producto_venta, name='eliminar_producto_venta'),
    path('eliminar/<int:venta_id>/', views.eliminar_venta, name='eliminar_venta'),
    path('crear_excel/', views.crear_excel, name='crear_excel'),
]