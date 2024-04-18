from django.db import models
from django.conf import settings
# Create your models here.

#Tabla Habitaciones 
class Habitaciones(models.Model):
    HAB_CATEGORIA=(
        ('Turista','Turista'),
        ('Premiun','Premiun'))
    ESTADO_OPCIONES = ((
        ('Disponible', 'Disponible'),
        ('No disponible', 'No disponible'),
    ))
    numero = models.IntegerField()
    capacidad = models.IntegerField()
    descripción = models.TextField()
    precio = models.IntegerField()
    categoria = models.CharField(max_length=20, choices=HAB_CATEGORIA)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES)
    
    def __str__(self):
        return f"Habitacion #{self.numero} de categoria {self.categoria} con capacidad para {self.capacidad} personas"

#Tabla Reservas
class Reservas(models.Model):
    ESTADO_RESERVAS = (
        ('Confirmada', 'Confirmada'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitaciones,on_delete=models.CASCADE )
    fecha_inicio = models.DateTimeField() #check in llegada
    fecha_fin = models.DateTimeField() #check out salida
    estado = models.CharField(max_length=20, choices=ESTADO_RESERVAS)

    def __str__(self):
        return f'{self.user} a reservado la {self.habitacion} desde {self.fecha_inicio} hasta {self.fecha_fin}'
    