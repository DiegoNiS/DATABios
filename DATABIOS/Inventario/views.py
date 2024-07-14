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
import datetime
# bd
from django.db import transaction, IntegrityError, DatabaseError


# Vista para listar productos (para vendedor y administrador)    
@login_required
def listar_productos(request):
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
    categorias = Categoria.objects.all().order_by('id')
    if request.method == 'POST':
        nombre_Prod_C = request.POST.get('nombre_Prod_C')
        categorias_ids_Prod_C = request.POST.getlist('categorias_Prod_C')
        stock_Prod_C = request.POST.get('stock_Prod_C')
        precio_compra_Prod_C = request.POST.get('precio_compra_Prod_C')
        precio_venta_Prod_C = request.POST.get('precio_venta_Prod_C')
        stock_min_Prod_C = request.POST.get('stock_min_Prod_C')
        stock_max_Prod_C = request.POST.get('stock_max_Prod_C')
        
        # Validaciones manuales
        errores = []
        if not nombre_Prod_C:
            errores.append('El campo nombre es obligatorio.')
        if not categorias_ids_Prod_C:
            errores.append('Debe seleccionar al menos una categoría.')
        if not stock_Prod_C or int(stock_Prod_C) <= 0:
            errores.append('El campo stock debe ser mayor que cero.')
        if not precio_compra_Prod_C or float(precio_compra_Prod_C) <= 0:
            errores.append('El campo precio de compra debe ser mayor que cero.')
        if not precio_venta_Prod_C or float(precio_venta_Prod_C) <= 0:
            errores.append('El campo precio de venta debe ser mayor que cero.')
        if not stock_min_Prod_C or int(stock_min_Prod_C) <= 0:
            errores.append('El campo stock mínimo debe ser mayor que cero.')
        if not stock_max_Prod_C or int(stock_max_Prod_C) <= 0:
            errores.append('El campo stock máximo debe ser mayor que cero.')
        if stock_min_Prod_C and stock_max_Prod_C and int(stock_min_Prod_C) > int(stock_max_Prod_C):
            errores.append('El campo stock mínimo no puede ser mayor que el stock máximo.')
        
        if nombre_Prod_C and categorias_ids_Prod_C and stock_Prod_C and precio_compra_Prod_C and precio_venta_Prod_C and precio_venta_Prod_C and stock_min_Prod_C and stock_max_Prod_C:
            try:
                with transaction.atomic():
                    producto = Producto(
                        nombre = nombre_Prod_C,
                        stock = stock_Prod_C,
                        precio_compra = precio_compra_Prod_C,
                        precio_venta = precio_venta_Prod_C,
                        stock_min = stock_min_Prod_C,
                        stock_max = stock_max_Prod_C
                    )
                    producto.save()
                    producto.categorias.set(categorias_ids_Prod_C)
                    messages.success(request, 'Producto creado exitosamente.')
                    return redirect('listar_productos')
            except IntegrityError as e:
                messages.error(request, f'Error de integridad: {e}')
            except DatabaseError as e:
                messages.error(request, f'Error de base de datos: {e}')
            except Exception as e:
                messages.error(request, f'Ocurrió un error inesperado: {e}')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = ProductoForm()

    return render(request, 'Inventario/crear_producto.html', {'categorias': categorias})

# Vista para editar un producto
@permisos_para(lambda u:u.id_permisos.inventario_pro_CUD)
def editar_producto(request, pk):
    try:
        producto = get_object_or_404(Producto, pk=pk)
        if request.method == 'POST':
            form = ProductoForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto modificado exitosamente.')
                return redirect('listar_productos')
            else:
                messages.error(request, 'Error en el formulario. Por favor, verifica los datos ingresados.')
        else:
            form = ProductoForm(instance=producto)
    except Producto.DoesNotExist:
        messages.error(request, 'El producto no existe.')
        return redirect('listar_productos')
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error: {str(e)}')
        return redirect('listar_productos')
    
    return render(request, 'Inventario/editar_producto.html', {'form': form, 'producto': producto})

# Vista para eliminar un producto
@permisos_para(lambda u:u.id_permisos.inventario_pro_CUD)
def eliminar_producto(request, pk):    
    try:
        producto = get_object_or_404(Producto, pk=pk)
        if request.method == 'POST':
            producto.delete()
            messages.success(request, 'Producto eliminado exitosamente.')
            return redirect('listar_productos')
    except Producto.DoesNotExist:
        messages.error(request, 'El producto no existe.')
        return redirect('listar_productos')
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error: {str(e)}')
        return redirect('listar_productos')
    
    return render(request, 'Inventario/eliminar_producto.html', {'producto': producto})


# Exportar Excel de Productos
@login_required
def exportar_productos_excel(request):
    try:
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
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error al exportar: {str(e)}')
        return redirect('listar_productos')

    return HttpResponse(status=400)


########### CATEGORIAS ##########

# Vista para listar categorías (para vendedor y administrador)
@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all().order_by('id')
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
    return render(request, 'Inventario/eliminar_categoria.html', {'categoria': categoria})
