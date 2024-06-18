from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


def list_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {
        'usuarios': usuarios
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def agregar_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
        else:
            return render(request, 'agregar_usuario.html', {'form': form, 'error': 'Por favor corrige los errores abajo.'})
    else:
        form = UserCreationForm()
    return render(request, 'agregar_usuario.html', {'form': form})

def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lista_usuarios')  # Redirige a la lista de usuarios después de iniciar sesión
        else:
            return render(request, 'usuarios/login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'login.html')

def cerrar_sesion(request):
    logout(request)
    # Redirigir a la página de inicio o a donde desees después del cierre de sesión
    return redirect('login')

# Max's Creations

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
