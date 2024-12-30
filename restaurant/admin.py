from django.contrib import admin

# Register your models here.

from .models import Plato, Mesa, Reserva



@admin.register(Plato)

class postPlato(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'descripcion', 'precio')
    list_filter = ('categoria', 'nombre')

@admin.register(Mesa)
class postMesa(admin.ModelAdmin):
    list_display = ('numero', 'capacidad')
    list_filter = ('capacidad', 'numero')

@admin.register(Reserva)
class postReserva(admin.ModelAdmin):
    list_display = ('mesa', 'fecha', 'hora')
    list_filter = ('mesa', 'fecha', 'hora')
