# Proyecto/Inventario/forms.py

from django import forms
from Core.models import Producto, Categoria, Pedido

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['categorias', 'nombre', 'stock', 'precio_compra', 'precio_venta', 'stock_min', 'stock_max']
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
