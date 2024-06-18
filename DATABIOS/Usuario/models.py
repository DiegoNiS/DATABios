from django.db import models

# Create your models here.

class Pedido(models.Model):
    # Define tus campos aquí
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    class Meta:
        permissions = [
            ("eliminar_pendientes", "Puede eliminar pendientes en la tabla pedidos"),
            ("editar_pendientes", "Puede editar pendientes en la tabla pedidos"),
            ("agregar_pendientes", "Puede agregar pendientes en la tabla pedidos"),
            ("confirmar_pendientes", "Puede confirmar pendientes en la tabla pedidos"),
            ("eliminar_registro_pedidos", "Puede eliminar registro de pedidos en la tabla pedidos"),
            ("generar_reportes_registro_pedidos", "Puede generar reportes de registro de pedidos en la tabla pedidos"),
        ]

class Producto(models.Model):
    # Define tus campos aquí
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    class Meta:
        permissions = [
            ("editar_productos", "Puede editar productos en la tabla inventario"),
            ("eliminar_productos", "Puede eliminar productos en la tabla inventario"),
            ("agregar_productos", "Puede agregar productos en la tabla inventario"),
            ("generar_reportes_productos", "Puede generar reportes de productos en la tabla inventario"),
        ]

class Venta(models.Model):
    # Define tus campos aquí
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    class Meta:
        permissions = [
            ("eliminar_ventas", "Puede eliminar ventas en la tabla ventas"),
            ("agregar_ventas", "Puede agregar ventas en la tabla ventas"),
            ("generar_reportes_ventas", "Puede generar reportes de ventas en la tabla ventas"),
        ]
