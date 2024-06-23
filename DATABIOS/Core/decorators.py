
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
                # Redireccionar a la página de permisos denegados
                return render(request, 'permisos_denegados.html')

        return wrapper

    return decorator