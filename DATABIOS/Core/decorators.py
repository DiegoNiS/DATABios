<<<<<<< HEAD

=======
from django.shortcuts import redirect
from django.contrib import messages
>>>>>>> Ower-Rama
from functools import wraps
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Core.models import Usuario

def permisos_para(permiso_check):
    def check_permiso(user):
        try:
            return user.is_authenticated and permiso_check(user)
        except Usuario.DoesNotExist:
            return False

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if check_permiso(request.user):
                return view_func(request, *args, **kwargs)
            else:
<<<<<<< HEAD
                # Redireccionar a la página de permisos denegados
                return render(request, 'permisos_denegados.html')

        return wrapper

    return decorator
=======
                return render(request, 'permisos_denegados.html')
        return wrapper
    return decorator


def ventas_permission_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.id_permisos.ventas_CD:
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
>>>>>>> Ower-Rama
