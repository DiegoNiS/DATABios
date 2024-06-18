# usuarios/forms.py

from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    CATEGORIA_CHOICES = (
        ('Administrador', 'Administrador'),
        ('Vendedor', 'Vendedor'),
    )
    categoria = forms.ChoiceField(choices=CATEGORIA_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'categoria')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        categoria = self.cleaned_data['categoria']
        
        # Aquí puedes agregar lógica adicional para definir permisos y grupos
        if categoria == 'Administrador':
            grupo = Group.objects.get(name='Administrador')
        else:
            grupo = Group.objects.get(name='Vendedor')
        
        if commit:
            user.save()
            user.groups.add(grupo)
        return user
