# Proyecto/inventario/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Core.models import Categoria, Producto
from .forms import ProductoForm, CategoriaForm

# Vista para listar productos (para vendedor y administrador)
@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    categoria_id = None
    precio_min = None
    precio_max = None
    mostrar_todos = False
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        precio_min = request.POST.get('precio_min')
        precio_max = request.POST.get('precio_max')
        mostrar_todos = request.POST.get('mostrar_todos') == 'on'
        if not mostrar_todos: # Si mostrar todos no esta activo
            if categoria_id:
                productos = productos.filter(categorias = categoria_id)
            if precio_min:
                productos = productos.filter(precio_venta__gte=precio_min)
            if precio_max:
                productos = productos.filter(precio_venta__lte=precio_max)
    categorias = Categoria.objects.all()
    return render(request, 'Inventario/listar_productos.html', {
        'productos': productos,
        'categorias':categorias,
        'categoria_id':categoria_id,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'mostrar_todos': mostrar_todos,
        })

# Vista para crear un nuevo producto 
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'Inventario/crear_producto.html', {'form': form})

# Vista para modificar un producto
@login_required
def modificar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto modificado exitosamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'Inventario/modificar_producto.html', {'form': form, 'producto': producto})

# Vista para eliminar un producto
@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('listar_productos')
    return render(request, 'Inventario/eliminar_producto.html', {'producto': producto})

# Vista para listar categorías (para vendedor y administrador)
@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'Inventario/listar_categorias.html', {'categorias': categorias})

# Vista para crear una nueva categoría
@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'Inventario/crear_categoria.html', {'form': form})

# Vista para modificar una categoría
@login_required
def modificar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría modificada exitosamente.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'Inventario/modificar_categoria.html', {'form': form, 'categoria': categoria})

# Vista para eliminar una categoría
@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('listar_categorias')
    return render(request, 'Inventario/eliminar_categoria.html', {'categoria': categoria})
