from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import ValidationError
from django.utils import timezone  # Importar timezone

class ConjuntoPermisos(models.Model):                       # added by Diego
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

class UsuarioManager(BaseUserManager):                      # added by Diego
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


class Usuario(AbstractBaseUser, PermissionsMixin):          # added by Diego
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=15, unique=True)
    nombre = models.CharField(max_length=18)
    apellido = models.CharField(max_length=18)
    categoria = models.CharField(max_length=18)
    id_permisos = models.OneToOneField(ConjuntoPermisos, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categorias = models.ManyToManyField(Categoria)
    nombre = models.CharField(max_length=100)
    stock = models.IntegerField()
    precio_compra = models.FloatField()
    precio_venta = models.FloatField()
    stock_min = models.IntegerField(default=10)
    stock_max = models.IntegerField(default=20)
    
    @property
    def estado_stock(self):
        if self.stock < self.stock_min:
            return 'bajo'
        elif self.stock > self.stock_max:
            return 'alto'
        else:
            return 'normal'

    def clean(self):
        super().clean()
        print("Ejecutando clean() en Producto")
        
        try:
            # Convertir valores a los tipos adecuados
            stock = int(self.stock)
            precio_compra = float(self.precio_compra)
            precio_venta = float(self.precio_venta)
            stock_min = int(self.stock_min)
            stock_max = int(self.stock_max)

            if stock < 0:
                print("Error: El valor de stock debe ser mayor o igual que cero.")
                raise ValidationError({'stock': 'El valor de stock debe ser mayor o igual que cero.'})
            if precio_compra <= 0:
                print("Error: El precio de compra debe ser mayor que cero.")
                raise ValidationError({'precio_compra': 'El precio de compra debe ser mayor que cero.'})
            if precio_venta <= 0:
                print("Error: El precio de venta debe ser mayor que cero.")
                raise ValidationError({'precio_venta': 'El precio de venta debe ser mayor que cero.'})
            if stock_min <= 0:
                print("Error: El valor de stock mínimo debe ser mayor que cero.")
                raise ValidationError({'stock_min': 'El valor de stock mínimo debe ser mayor que cero.'})
            if stock_max <= 0:
                print("Error: El valor de stock máximo debe ser mayor que cero.")
                raise ValidationError({'stock_max': 'El valor de stock máximo debe ser mayor que cero.'})
            if stock_min > stock_max:
                print("Error: El valor de stock mínimo no puede ser mayor que el stock máximo.")
                raise ValidationError({'stock_min': 'El valor de stock mínimo no puede ser mayor que el stock máximo.'})
        except ValidationError as e:
            print(f"ValidationError: {e}")
            raise
        except Exception as e:
            print(f"Ocurrió un error inesperado en clean: {e}")
            raise
        
        print("Fin clean()")
        
    def __str__(self):
        return self.nombre