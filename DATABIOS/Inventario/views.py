# Proyecto/inventario/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from Core.models import Categoria, Producto, Pedido, Proveedores
from .forms import ProductoForm, CategoriaForm, PedidoForm, ActualizarEstadoPedidoForm, ProveedoresForm

# Vista para listar productos (para vendedor y administrador)
@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar_productos.html', {'productos': productos})

# Vista para crear un nuevo producto (solo para administrador)
@login_required
def crear_producto(request):
    #if request.user.groups.filter(name='Administrador').exists():
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})
    '''
    else:
        messages.error(request, 'No tiene permisos para crear productos.')
        return redirect('listar_productos')
    '''
# Vista para listar categorías (para vendedor y administrador)
@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'listar_categorias.html', {'categorias': categorias})

# Vista para crear una nueva categoría (solo para administrador)
@login_required
def crear_categoria(request):
    #if request.user.groups.filter(name='Administrador').exists():
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'crear_categoria.html', {'form': form})
    """
    else:
        messages.error(request, 'No tiene permisos para crear categorías.')
        return redirect('listar_categorias')
    """
"""
@login_required
def listar_pedidos(request):
    listar_pedidos = Pedido.objects.all()
    return render(request, 'listar_pedidos.html', {'listar_pedidos': listar_pedidos})
"""
@login_required
def listar_pedidos(request):
    if request.method == 'POST':
        form = ActualizarEstadoPedidoForm(request.POST)
        if form.is_valid():
            pedido_id = request.POST.get('pedido_id')
            pedido = get_object_or_404(Pedido, id=pedido_id)
            pedido.estado = form.cleaned_data['estado']
            pedido.save()
            return redirect('listar_pedidos')  # Asegúrate de que el nombre de tu URL coincida
    else:
        form = ActualizarEstadoPedidoForm()
    
    listar_pedidos = Pedido.objects.all()
    return render(request, 'listar_pedidos.html', {'listar_pedidos': listar_pedidos, 'form': form})
"""""
@login_required
def crear_pedidos(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido creado exitosamente.')
            return redirect('listar_pedidos')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = PedidoForm()
    
    return render(request, 'crear_pedidos.html', {'form': form})
"""
def crear_pedidos(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.total = pedido.cantidad * pedido.precio_unitario
            pedido.save()
            form.save_m2m()  # Guardar relaciones ManyToMany
            messages.success(request, 'Pedido creado exitosamente.')
            return redirect('listar_pedidos')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = PedidoForm()
    
    return render(request, 'crear_pedidos.html', {'form': form})

@login_required
def crear_proveedores(request):
    if request.method == 'POST':
        form = ProveedoresForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('listar_proveedores')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ProveedoresForm()
    
    return render(request, 'crear_proveedores.html', {'form': form})


@login_required
def listar_proveedores(request):
    listar_proveedores = Proveedores.objects.all()
    form = ProveedoresForm()
    return render(request, 'listar_proveedores.html', {'listar_proveedores': listar_proveedores, 'form': form})