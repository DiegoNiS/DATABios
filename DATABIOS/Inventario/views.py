# Proyecto/Inventario/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from Core.models import Categoria, Producto
from Core.decorators import permisos_para
from .forms import ProductoForm, CategoriaForm
# excel
import openpyxl
from io import BytesIO
<<<<<<< HEAD
import datetime
=======
>>>>>>> Ower-Rama


# Vista para listar productos (para vendedor y administrador)    
@login_required
def listar_productos(request):
<<<<<<< HEAD
    productos = Producto.objects.all().order_by('id')
    categorias = Categoria.objects.all()

    # Obtener parámetros GET para filtrar
    categoria_id = request.GET.get('filtro_categoria')
    precio_min = request.GET.get('filtro_precio_min')
    precio_max = request.GET.get('filtro_precio_max')
    estado_stock = request.GET.get('filtro_estado_stock')
    mostrar_todos = request.GET.get('filtro_mostrar_todos') == 'on'

    if not mostrar_todos:  # Si mostrar todos no está activo
        if categoria_id:
            productos = productos.filter(categorias=categoria_id)
        if precio_min:
            productos = productos.filter(precio_venta__gte=precio_min)
        if precio_max:
            productos = productos.filter(precio_venta__lte=precio_max)
        if estado_stock:
            productos = [p for p in productos if p.estado_stock == estado_stock]

    """
    # Manejar la solicitud AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {'productos': productos}
        html = render_to_string('Inventario/tabla_productos.html', context)
        return JsonResponse({'html': html})
    """
    return render(request, 'Inventario/listar_productos.html', {
        'productos': productos,
        'categorias': categorias,
    })
"""
por ahora se esta usando el metodo get
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
"""
# !!!!?
@login_required
=======
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
# !!!!?
@login_required
>>>>>>> Ower-Rama
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

# Vista para editar un producto
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

# Exportar Excel de Productos
@login_required
def exportar_productos_excel(request):
<<<<<<< HEAD
    if request.method == 'POST':
        producto_ids = request.POST.get('producto_ids').split(',')
        productos = Producto.objects.order_by('id').filter(id__in=producto_ids)
    
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Productos'
        
        encabezados = ['ID', 'Nombre', 'Categoria', 'Stock', 'Precio Compra', 'Precio Venta', 'Estado Stock']
        ws.append(encabezados)
        
        # Escribir datos
        for producto in productos:
            categorias = ', '.join([str(c) for c in producto.categorias.all()])
            ws.append([
                producto.id,
                producto.nombre,
                categorias,
                producto.stock,
                producto.precio_compra,
                producto.precio_venta,
                producto.estado_stock
            ])
        
        # Guardar el archivo en memoria
        archivo = BytesIO()
        wb.save(archivo)
        archivo.seek(0)
        
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y%m%d_%H%M%S")
        filename = f'productos_{formatted_date}.xlsx'
        
        response = HttpResponse(
            archivo,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
        return response
    return HttpResponse(status = 400)
=======
    productos = Producto.objects.all()
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Productos'
    
    encabezados = ['ID', 'Nombre', 'Categoria', 'Stock', 'Precio Compra', 'Precio Venta', 'Estado Stock']
    ws.append(encabezados)
    
    # Escribir datos
    for producto in productos:
        categorias = ', '.join([str(c) for c in producto.categorias.all()])
        ws.append([
            producto.id,
            producto.nombre,
            categorias,
            producto.stock,
            producto.precio_compra,
            producto.precio_venta,
            producto.estado_stock
        ])
    
    # Guardar el archivo en memoria
    archivo = BytesIO()
    wb.save(archivo)
    archivo.seek(0)
    
    response = HttpResponse(
        archivo,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=productos.xlsx'
    return response
>>>>>>> Ower-Rama

########### CATEGORIAS ##########

# Vista para listar categorías (para vendedor y administrador)
@login_required
def listar_categorias(request):
<<<<<<< HEAD
    categorias = Categoria.objects.all().order_by('id')
=======
    categorias = Categoria.objects.all()
>>>>>>> Ower-Rama
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

# Vista para editar una categoría
@permisos_para(lambda u:u.id_permisos.inventario_cat_CUD)
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría modificada exitosamente.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'Inventario/editar_categoria.html', {'form': form, 'categoria': categoria})

# Vista para eliminar una categoría
@permisos_para(lambda u:u.id_permisos.inventario_cat_CUD)
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('listar_categorias')
<<<<<<< HEAD
    return render(request, 'Inventario/eliminar_categoria.html', {'categoria': categoria})
=======
    return render(request, 'Inventario/eliminar_categoria.html', {'categoria': categoria})
>>>>>>> Ower-Rama
