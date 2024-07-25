from django.shortcuts import render
from .forms import PedidoForm, ActualizarEstadoPedidoForm, ProveedoresForm
from Core.models import Pedido, Producto
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

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