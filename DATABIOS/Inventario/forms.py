# Proyecto/inventario/forms.py

from django import forms
from Core.models import Producto, Categoria

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
