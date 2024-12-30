"""
URL configuration for restaurant_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from restaurant.views import menu, base, mesas, reservas, eliminar_mesa, ver_plato, eliminar_plato, editar_plato, ver_reserva, eliminar_reserva, editar_reserva, about_me
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', view=base, name='base'),
    path('about_me/', view=about_me, name='about_me'),
    path('menu/', view=menu, name='menu'),
    path('ver_plato/<int:plato_id>/', view=ver_plato, name='ver_plato'),
    path('eliminar_plato/<int:plato_id>/', view=eliminar_plato, name='eliminar_plato'),
    path('editar_plato/<int:plato_id>/', view=editar_plato, name='editar_plato'),
    path('mesas/', mesas, name='mesas'),
    path('eliminar_mesa/<int:mesa_id>/', eliminar_mesa, name='eliminar_mesa'),
    path('reservas/', reservas, name='reservas'), 
    path('ver_reserva/<int:reserva_id>/', ver_reserva, name='ver_reserva'),
    path('editar_reserva/<int:reserva_id>/', editar_reserva, name='editar_reserva'),
    path('eliminar_reserva/<int:reserva_id>/', eliminar_reserva, name='eliminar_reserva'), 
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

