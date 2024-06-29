# Proyecto/Inventario/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from Core.models import Categoria, Producto
from Core.decorators import permisos_para
from .forms import ProductoForm, CategoriaForm

# Vista para listar productos (para vendedor y administrador)    
@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()            
    # estado de stock de cada producto segun el filtro
    return render(request, 'Inventario/listar_productos.html', {
        'productos': productos,
        'categorias':categorias,
        })
    
@login_required
def filtrar_productos(request):
    productos = Producto.objects.all()
    categoria_id = request.POST.get('filtro_categoria')
    precio_min = request.POST.get('filtro_precio_min')
    precio_max = request.POST.get('filtro_precio_max')
    estado_stock = request.POST.get('filtro_estado_stock')
    mostrar_todos = request.POST.get('filtro_mostrar_todos') == 'on'
    
    if not mostrar_todos:  # Si mostrar todos no está activo
        if categoria_id:
            productos = productos.filter(categorias=categoria_id)
        if precio_min:
            productos = productos.filter(precio_venta__gte=precio_min)
        if precio_max:
            productos = productos.filter(precio_venta__lte=precio_max)
        if estado_stock:
            productos = [p for p in productos if p.estado_stock == estado_stock]

    context = {'productos': productos}
    html = render_to_string('Inventario/tabla_productos.html', context)
    return JsonResponse({'html': html})
    
@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, id=pk)
    data = {
        'nombre': producto.nombre,
        'stock': producto.stock,
        'precio_compra': producto.precio_compra,
        'precio_venta': producto.precio_venta,
    }
    return JsonResponse(data)

# Vista para crear un nuevo producto 
@permisos_para(lambda u:u.id_permisos.inventario_pro_CUD)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('listar_productos')
    else:
        form_crear_producto = ProductoForm()
    return render(request, 'Inventario/crear_producto.html', {'form_crear_producto': form_crear_producto})

# Vista para modificar un producto
@permisos_para(lambda u:u.id_permisos.inventario_pro_CUD)
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto modificado exitosamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'Inventario/editar_producto.html', {'form': form, 'producto': producto})

# Vista para eliminar un producto
@permisos_para(lambda u:u.id_permisos.inventario_pro_CUD)
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
@permisos_para(lambda u:u.id_permisos.inventario_cat_CUD)
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
@permisos_para(lambda u:u.id_permisos.inventario_cat_CUD)
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
@permisos_para(lambda u:u.id_permisos.inventario_cat_CUD)
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('listar_categorias')
    return render(request, 'Inventario/eliminar_categoria.html', {'categoria': categoria})
