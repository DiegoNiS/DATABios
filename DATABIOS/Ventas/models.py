# ventas/models.py
from django.db import models

class Vendedor(models.Model):
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Venta(models.Model):
    descripcion = models.TextField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    fecha_creacion = models.DateField()

    def __str__(self):
        return f"Venta {self.id} - {self.descripcion}"
