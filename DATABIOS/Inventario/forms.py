# Proyecto/inventario/forms.py

from django import forms
from django.core.exceptions import ValidationError
from Core.models import Producto, Categoria, Pedido

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['categorias', 'nombre', 'stock', 'precio_compra', 'precio_venta']
        widgets = {
            'categorias': forms.CheckboxSelectMultiple(),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
    
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['categoria', 'productos', 'cantidad', 'precio_unitario', 'estado']
        widgets = {
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'productos': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise ValidationError('La cantidad no puede ser cero o menor.')
        return cantidad
    
    def clean_precio_unitario(self):
        precio_unitario = self.cleaned_data.get('precio_unitario')
        if precio_unitario <= 0:
            raise ValidationError('El precio unitario debe ser mayor a 0.00.')
        return precio_unitario