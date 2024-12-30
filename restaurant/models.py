from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Plato(models.Model):
    CATEGORIAS = [
        ('principal', 'Plato Principal'),
        ('guarnicion', 'Guarnicion'),
        ('postre', 'Postre'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)

    def __str__(self):
        return self.nombre


class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return f"Mesa {self.numero} (Capacidad: {self.capacidad})"


class Reserva(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"Reserva de {self.nombre_cliente} en {self.fecha} a las {self.hora}"
