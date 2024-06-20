# ventas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Venta, Vendedor
from .forms import VentaForm


def ventas_list(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas_list.html', {'ventas': ventas})

def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ventas_list')
    else:
        form = VentaForm()
    return render(request, 'venta_form.html', {'form': form})

def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('ventas_list')
    return render(request, 'venta_confirm_delete.html', {'venta': venta})

def export_to_excel(request):
    # Aquí iría la lógica para exportar a Excel
    return HttpResponse('Función para exportar a Excel aún no implementada')


