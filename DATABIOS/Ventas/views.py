# ventas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Venta
from Core.models import Usuario
from django.contrib import messages
from django.db.models import Q


def ventas_list(request):
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

def venta_create(request):
    if request.method == 'POST':
        descripcion = request.POST['description']
        vendedor = request.POST['vendedor']
        fecha = request.POST['fecha']
        if descripcion is not None and vendedor is not None and fecha is not None: # TODO:  aca deberiamos confirmar campo por campo que todo sea correcto para aceptar los campos
            venta = Venta()
            venta.descripcion = descripcion
            venta.fecha_creacion = fecha
            venta.vendedor = get_object_or_404(Usuario, username = vendedor)
            venta.save()
            messages.success(request, "Campo registrado exitosamente")
            return redirect('ventas_list')
        else: 
            messages.error(request, "Los campos no fueron rellenados correctamente")
            return redirect('venta_create')
    else:
        vends = Usuario.objects.all()
        return render(request, 'venta_form.html', {
            'vends' : vends,
        })
        #form = VentaForm()
    #return render(request, 'venta_form.html', {'form': form})

def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('ventas_list')
    return render(request, 'venta_confirm_delete.html', {'venta': venta})

def export_to_excel(request):
    # Aquí iría la lógica para exportar a Excel
    return HttpResponse('Función para exportar a Excel aún no implementada')


