# Proyecto/Inventario/views.py
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from Core.models import Categoria, Producto, Pedido, Proveedores
from Core.decorators import permisos_para
from .forms import ProductoForm, CategoriaForm, PedidoForm, ActualizarEstadoPedidoForm, ProveedoresForm

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
    categorias = Categoria.objects.all().order_by('id')
    proveedores = Proveedores.objects.all().order_by('id')
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
    else:
        redirect('listar_productos')

    return render(request, 'Inventario/listar_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'proveedores': proveedores,
    })

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
# Validadar errores formulario producto
def validar_datos_producto(nombre, categorias_ids, proveedor_id, stock, precio_compra, precio_venta, stock_min, stock_max):
    errores = []
    if not nombre:
        errores.append('El campo nombre es obligatorio.')
    if not categorias_ids:
        errores.append('Debe seleccionar al menos una categoría.')
    if not proveedor_id:
        errores.append('Debe de seleccionar un un proveedor')
    if not stock or int(stock) <= 0:
        errores.append('El campo stock debe ser mayor que cero.')
    if not precio_compra or float(precio_compra) <= 0:
        errores.append('El campo precio de compra debe ser mayor que cero.')
    if not precio_venta or float(precio_venta) <= 0:
        errores.append('El campo precio de venta debe ser mayor que cero.')
    if not stock_min or int(stock_min) <= 0:
        errores.append('El campo stock mínimo debe ser mayor que cero.')
    if not stock_max or int(stock_max) <= 0:
        errores.append('El campo stock máximo debe ser mayor que cero.')
    if stock_min and stock_max and int(stock_min) > int(stock_max):
        errores.append('El campo stock mínimo no puede ser mayor que el stock máximo.')
    return errores

# Vista para crear un nuevo producto 
@permisos_para(lambda u:u.id_permisos.inventario_pro_CUD)
def crear_producto(request):
    categorias = Categoria.objects.all().order_by('id')
    proveedores = Proveedores.objects.all().order_by('id') 
    if request.method == 'POST':
        nombre_Prod_C = request.POST.get('nombre_Prod_C')
        categorias_ids_Prod_C = request.POST.getlist('categorias_Prod_C')
        proveedor_id_Prod_C = request.POST.get('proveedor_Prod_C')
        stock_Prod_C = request.POST.get('stock_Prod_C')
        precio_compra_Prod_C = request.POST.get('precio_compra_Prod_C')
        precio_venta_Prod_C = request.POST.get('precio_venta_Prod_C')
        stock_min_Prod_C = request.POST.get('stock_min_Prod_C')
        stock_max_Prod_C = request.POST.get('stock_max_Prod_C')
        
        # Validaciones manuales
        errores = validar_datos_producto(nombre_Prod_C, categorias_ids_Prod_C, proveedor_id_Prod_C, stock_Prod_C, precio_compra_Prod_C, precio_venta_Prod_C, stock_min_Prod_C, stock_max_Prod_C)
        
        if not errores:
            try:
                with transaction.atomic(): # Agregar por transaccion
                    producto = Producto(
                        nombre = nombre_Prod_C,
                        proveedor_id=proveedor_id_Prod_C,
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

    return render(request, 'Inventario/crear_producto.html', {'categorias': categorias, 'proveedores': proveedores})

# Vista para editar un producto
@permisos_para(lambda u: u.id_permisos.inventario_pro_CUD)
def editar_producto(request, pk):
    productos = Producto.objects.all().order_by('id')
    try:
        producto = get_object_or_404(Producto, pk=pk)
        categorias = Categoria.objects.all().order_by('id')
        proveedores = Proveedores.objects.all().order_by('id')
        if request.method == 'POST':
            # Recuperar los datos enviados en el formulario
            nombre_Prod_E = request.POST.get('nombre_Prod_E')
            categorias_ids_Prod_E = request.POST.getlist('categorias_Prod_E')
            proveedor_id = int(request.POST.get('proveedor_Prod_E'))
            proveedor_id_Prod_E = get_object_or_404(Proveedores, id=proveedor_id)
            stock_Prod_E = request.POST.get('stock_Prod_E')
            precio_compra_Prod_E = request.POST.get('precio_compra_Prod_E')
            precio_venta_Prod_E = request.POST.get('precio_venta_Prod_E')
            stock_min_Prod_E = request.POST.get('stock_min_Prod_E')
            stock_max_Prod_E = request.POST.get('stock_max_Prod_E')

            # Validar los datos
            errores = validar_datos_producto(nombre_Prod_E, categorias_ids_Prod_E, proveedor_id_Prod_E, stock_Prod_E, precio_compra_Prod_E, precio_venta_Prod_E, stock_min_Prod_E, stock_max_Prod_E)

            if not errores:
                try:
                    with transaction.atomic():
                        producto.nombre = nombre_Prod_E
                        producto.proveedor = proveedor_id_Prod_E
                        producto.stock = stock_Prod_E  # Cambiado para corregir la asignación
                        producto.precio_compra = precio_compra_Prod_E
                        producto.precio_venta = precio_venta_Prod_E
                        producto.stock_min = stock_min_Prod_E
                        producto.stock_max = stock_max_Prod_E
                        print(producto.nombre)
                        print("antes de clean")
                        producto.clean()  # Llamar a las validaciones del modelo
                        print("Despues del clean")
                        producto.save()
                        producto.categorias.set(categorias_ids_Prod_E)
                        messages.success(request, 'Producto modificado exitosamente.')
                        return redirect('listar_productos')
                except ValidationError as e:
                    messages.error(request, f'Error de validación: {e}')
                    print("Error de validadcion")
                except IntegrityError as e:
                    messages.error(request, f'Error de integridad: {e}')
                    print("Error de Integridad")
                except DatabaseError as e:
                    messages.error(request, f'Error de base de datos: {e}')
                    print("Error de base de datos")
                except Exception as e:
                    messages.error(request, f'Ocurrió un error inesperado: {e}')
                    print("Otro error", e)
            else:
                for error in errores:
                    messages.error(request, error)
                    
        form = {
            'categorias': producto.categorias.values_list('id', flat=True),
        }
            
    except Producto.DoesNotExist:
        messages.error(request, 'El producto no existe.')
        return redirect('listar_productos')
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error: {str(e)}')
        return redirect('listar_productos')
    return redirect('listar_productos')


# Vista para eliminar un producto
@permisos_para(lambda u: u.id_permisos.inventario_pro_CUD)
def eliminar_producto(request, pk):    
    try:
        producto = get_object_or_404(Producto, pk=pk)
        if request.method == 'POST':
            try:
                producto.delete()
                messages.success(request, 'Producto eliminado exitosamente.')
                return redirect('listar_productos')
            except IntegrityError as e:
                messages.error(request, f'Error de integridad: {e}')
            except DatabaseError as e:
                messages.error(request, f'Error de base de datos: {e}')
                print("Error de base de datos: ", e)
            except Exception as e:
                messages.error(request, f'Ocurrió un error inesperado: {e}')
    except Producto.DoesNotExist:
        messages.error(request, 'El producto no existe.')
        return redirect('listar_productos')
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error: {str(e)}')
        return redirect('listar_productos')
    return redirect('listar_productos')
    #return render(request, 'Inventario/eliminar_producto.html', {'producto': producto})


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

@login_required
def notificar_stock_bajo():
    numero = 1
    # Cuerpo de la funcion

########### CATEGORIAS ##########

# Vista para listar categorías (para vendedor y administrador)
@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all().order_by('id')
    return render(request, 'Inventario/listar_categorias.html', {'categorias': categorias})

# Vista para crear una nueva categoría
@permisos_para(lambda u: u.id_permisos.inventario_cat_CUD)
def crear_categoria(request):
    if request.method == 'POST':
        nombre_Cat_C = request.POST.get('nombre_Cat_C')
        descripcion_Cat_C = request.POST.get('descripcion_Cat_C')

        try:
            with transaction.atomic():
                categoria = Categoria(
                    nombre=nombre_Cat_C, 
                    descripcion=descripcion_Cat_C
                )
                categoria.save()
                messages.success(request, 'Categoría creada exitosamente.')
                return redirect('listar_categorias')
        except ValidationError as e:
            messages.error(request, f'Error de validación al crear la categoría: {e}')
        except IntegrityError as e:
            messages.error(request, f'Error de integridad al crear la categoría: {e}')
        except DatabaseError as e:
            messages.error(request, f'Error de base de datos al crear la categoría: {e}')
        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado al crear la categoría: {e}')

    return render(request, 'Inventario/crear_categoria.html')

# Vista para editar una categoría
@permisos_para(lambda u:u.id_permisos.inventario_cat_CUD)
def editar_categoria(request, pk):
    try:
        categoria = get_object_or_404(Categoria, pk=pk)

        if request.method == 'POST':
            nombre_Cat_E = request.POST.get('nombre_Cat_E')
            descripcion_Cat_E = request.POST.get('descripcion_Cat_E')

            try:
                with transaction.atomic():
                    categoria.nombre = nombre_Cat_E
                    categoria.descripcion = descripcion_Cat_E
                    categoria.save()
                    messages.success(request, 'Categoría modificada exitosamente.')
                    return redirect('listar_categorias')
            except ValidationError as e:
                messages.error(request, f'Error de validación al modificar la categoría: {e}')
            except IntegrityError as e:
                messages.error(request, f'Error de integridad al modificar la categoría: {e}')
            except DatabaseError as e:
                messages.error(request, f'Error de base de datos al modificar la categoría: {e}')
            except Exception as e:
                messages.error(request, f'Ocurrió un error inesperado al modificar la categoría: {e}')
        else:
            form = {
                "nombre": categoria.nombre,
                "descripcion": categoria.descripcion            
            }
    except Categoria.DoesNotExist:
        messages.error(request, 'El producto no existe.')
        return redirect('listar_categorias')
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error: {str(e)}')
        return redirect('listar_categorias')
    return render(request, 'Inventario/editar_categoria.html', {'categoria': categoria})

# Vista para eliminar una categoría
@permisos_para(lambda u: u.id_permisos.inventario_cat_CUD)
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                categoria.delete()
                messages.success(request, 'Categoría eliminada exitosamente.')
                return redirect('listar_categorias')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al eliminar la categoría: {e}')
    return redirect('eliminar_categoria')
    #return render(request, 'Inventario/eliminar_categoria.html', {'categoria': categoria})

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

#@login_required
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
