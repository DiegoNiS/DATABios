from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
<<<<<<< HEAD
from django.db.models import Q
=======
from .models import Venta, DetalleVenta
from Core.models import Usuario, Producto
from decimal import Decimal
>>>>>>> 56abafefa3d15a8862e4c433a8f526ec39b49008


@login_required
def ventas_list(request):
<<<<<<< HEAD
    vendedores = Usuario.objects.all()
    ventas = Venta.objects.all().order_by('-id')
    if request.method == 'POST':
        fdesde = request.POST['fecha1']
        fhasta = request.POST['fecha2']
        vend = request.POST['vendedor']

        filtros = Q()

        if fdesde and fhasta:
            filtros &= Q(fecha_creacion__range=[fdesde, fhasta])
        if vend and vend != "*":
            vendedor = get_object_or_404(Usuario, id=vend)
            filtros &= Q(vendedor=vendedor)

        if filtros:
            ventas = Venta.objects.filter(filtros).order_by('-id')
    return render(request, 'ventas_list.html', {
        'ventas': ventas,
        'vendedores': vendedores
    })
=======
    if not request.user.id_permisos.ventas_CD:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')  # Asume que tienes una vista 'home'
    
    venta = Venta.objects.all().order_by('-fecha_creacion')
    usuarios = Usuario.objects.all()
    return render(request, 'ventas/ventas_list.html', {'venta': venta, 'usuarios': usuarios})
>>>>>>> 56abafefa3d15a8862e4c433a8f526ec39b49008


@login_required
def venta_detail(request, venta_id):
    if not request.user.id_permisos.ventas_CD:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')
    
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'ventas/detalle_venta.html', {'venta': venta})


@login_required
def agregar_venta(request):
    if not request.user.id_permisos.ventas_CD:
        return JsonResponse({'error': 'No tienes permiso para realizar esta acción.'}, status=403)
    
    if request.method == 'POST':
        venta = Venta.objects.create(vendedor=request.user)
        return JsonResponse({'venta_id': venta.id})
    
    producto = Producto.objects.all()
    return render(request, 'ventas/agregar_venta.html', {'producto': producto})


@login_required
def agregar_producto_venta(request):
    if not request.user.id_permisos.ventas_CD:
        return JsonResponse({'error': 'No tienes permiso para realizar esta acción.'}, status=403)
    
    if request.method == 'POST':
        venta_id = request.POST.get('venta_id')
        producto_id = request.POST.get('producto_id')
        unidades = int(request.POST.get('unidades'))
        
        venta = get_object_or_404(Venta, id=venta_id)
        producto = get_object_or_404(Producto, id=producto_id)
        
        if producto.stock < unidades:
            return JsonResponse({'error': 'No hay suficiente stock disponible.'}, status=400)
        
        detalle = DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            unidades=unidades,
            precio_unitario=producto.precio_venta
        )
        
        producto.stock -= unidades
        producto.save()
        
        venta.total += detalle.importe
        venta.save()
        
        return JsonResponse({
            'id': detalle.id,
            'producto': producto.nombre,
            'precio_unitario': float(detalle.precio_unitario),
            'unidades': detalle.unidades,
            'importe': float(detalle.importe)
        })


@login_required
def eliminar_producto_venta(request, detalle_id):
    if not request.user.id_permisos.ventas_CD:
        return JsonResponse({'error': 'No tienes permiso para realizar esta acción.'}, status=403)
    
    detalle = get_object_or_404(DetalleVenta, id=detalle_id)
    venta = detalle.venta
    producto = detalle.producto
    
    producto.stock += detalle.unidades
    producto.save()
    
    venta.total -= detalle.importe
    venta.save()
    
    detalle.delete()
    return JsonResponse({'success': True})


@login_required
def eliminar_venta(request, venta_id):
    if not request.user.id_permisos.ventas_CD:
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('ventas_list')
    
    venta = get_object_or_404(Venta, id=venta_id)
    for detalle in venta.detalles.all():
        producto = detalle.producto
        producto.stock += detalle.unidades
        producto.save()
    
    venta.delete()
    messages.success(request, 'Venta eliminada con éxito.')
    return redirect('ventas_list')


@login_required
def crear_excel(request):
    if not request.user.id_permisos.ventas_CD:
        return JsonResponse({'error': 'No tienes permiso para realizar esta acción.'}, status=403)
    
    # Implementa la lógica para crear el Excel aquí
    
    messages.success(request, 'Excel creado exitosamente.')
    return JsonResponse({'success': True, 'message': 'Excel creado exitosamente'})
