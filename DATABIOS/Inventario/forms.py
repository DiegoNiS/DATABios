# Proyecto/inventario/forms.py

from django import forms
from django.core.exceptions import ValidationError
from Core.models import Producto, Categoria, Pedido, Proveedores

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

class ProveedorSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        if isinstance(label, Proveedores):
            label = label.nombre  # Mostrar solo el nombre del proveedor
        return super().create_option(name, value, label, selected, index, subindex, attrs)
    
class PedidoForm(forms.ModelForm):
    """
    proveedor = forms.ModelChoiceField(
        queryset=Proveedores.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        empty_label=None  # Esto evitará que aparezca una opción vacía en el desplegable
    
    )"""

    proveedor = forms.ModelChoiceField(
        queryset=Proveedores.objects.all(),
        widget=ProveedorSelect(attrs={'class': 'form-control'}),
        empty_label='Seleccione un proveedor'  # Texto opcional para el primer option
    )
    
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    
    class Meta:
            model = Pedido
            fields = ['categoria', 'proveedor', 'productos', 'cantidad', 'precio_unitario', 'descripcion']
            widgets = {
            #'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            #'productos': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            #'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        if 'proveedor' in self.data:
            try:
                proveedor_id = int(self.data.get('proveedor'))
                self.fields['productos'].queryset = Producto.objects.filter(proveedor__id=proveedor_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['productos'].queryset = self.instance.productos.all()
    """"
    def save(self, commit=True):
        pedido = super().save(commit=False)
        if commit:
            pedido.save()
            self.save_m2m()
        return pedido
    """
        #def __init__(self, *args, **kwargs):
         #   super().__init__(*args, **kwargs)
          #  if self.instance.pk:
           #     self.fields['proveedores'].queryset = self.obtener_proveedores()

        #def obtener_proveedores(self):
         #   proveedores = set()
          #  for producto in self.instance.productos.all():
           #     proveedores.add(producto.proveedor)
            #return proveedores
        #def obtener_proveedores(self):
         #   proveedores = Proveedores.objects.filter(producto__pedido=self.instance).distinct()
          #  return proveedores
      #  def obtener_proveedores(self):
       #     if self.instance.pk:
        #        return Proveedores.objects.filter(pedido=self.instance).distinct()
         #   return Proveedores.objects.none()

        #def save(self, commit=True):
         #   pedido = super().save(commit=False)
          #  if commit:
           #     pedido.save()
            #    self.save_m2m()  # Guardar relaciones ManyToMany
            #return pedido
        
        
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
    
class ActualizarEstadoPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'})
        }

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields = ['nombre', 'ruc', 'telefono']
        widgets = {
            
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            
        }