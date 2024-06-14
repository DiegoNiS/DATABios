from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.decorators import login_required, user_passes_test

#Creacion de grupos
def crear_grupos():
    Group.objects.get_or_create(name='Administrador')
    Group.objects.get_or_create(name='Vendedor')
    
def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

# Login view
def loginView(request):
    crear_grupos()  # Crear grupos si no existen
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')  # Redirigir al sistema

        else:
            messages.error(request, 'Credenciales inválidas')
            return redirect('/')
    else:
        return render(request, 'login.html')
    
    
# Vista de Home
@login_required
def homeView(request):
    usuario = request.user
    grupos_usuario = usuario.groups.values_list('name', flat=True)
    context = {
        'nombre_usuario': usuario.username,
        'grupos_usuario': list(grupos_usuario)
    }
    return render(request, 'home.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
