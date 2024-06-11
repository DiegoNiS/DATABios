from django.urls import path
from .views import loginView, homeView, logout

urlpatterns = [
    path('', loginView, name='login'),  # Login es la primera ruta
    path('home/', homeView, name='home'),
    path('logout/', logout, name='logout'),
]
