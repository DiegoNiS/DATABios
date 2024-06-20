# ventas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ventas_list, name='ventas_list'),
    path('create/', views.venta_create, name='venta_create'),
    path('<int:pk>/delete/', views.venta_delete, name='venta_delete'),
    path('export/', views.export_to_excel, name='export_to_excel'),
]
