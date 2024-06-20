# Usuario/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone  # Importar timezone

class ConjuntoPermisos(models.Model):
    pedidos_pen_CUD = models.BooleanField(default=False)
    pedidos_pen_S = models.BooleanField(default=False)
    pedidos_rec_G = models.BooleanField(default=False)
    inventario_cat_CUD = models.BooleanField(default=False)
    inventario_pro_CUD = models.BooleanField(default=False)
    inventario_pro_G = models.BooleanField(default=False)
    ventas_CD = models.BooleanField(default=False)
    panel_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"Permisos {self.id}"

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        
        # Determinar si el usuario es superusuario
        if extra_fields.get('is_superuser') is True:
            permisos = ConjuntoPermisos.objects.create(
                pedidos_pen_CUD=True,
                pedidos_pen_S=True,
                pedidos_rec_G=True,
                inventario_cat_CUD=True,
                inventario_pro_CUD=True,
                inventario_pro_G=True,
                ventas_CD=True,
                panel_admin=True,
            )
        else:
            permisos = ConjuntoPermisos.objects.create()
        extra_fields['id_permisos'] = permisos
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=15, unique=True)
    nombre = models.CharField(max_length=18)
    apellido = models.CharField(max_length=18)
    categoria = models.CharField(max_length=18)
    id_permisos = models.OneToOneField(ConjuntoPermisos, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)  # Agregar campo fecha_creacion
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
