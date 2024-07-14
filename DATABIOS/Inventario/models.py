from django.db import models

# Create your models here.

# Debe de estar Aplicacion Core por ahora en Inventario
'''
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categorias = models.ManyToManyField(Categoria)
    nombre = models.CharField(max_length=100)
    stock = models.IntegerField()
    precio_compra = models.FloatField()
    precio_venta = models.FloatField()

    def __str__(self):
        return self.nombre
'''