from django.db import models
from django.conf import settings
# Create your models here.

#Tabla Habitaciones 
class Habitaciones(models.Model):
    HAB_CATEGORIA = (
        ('Turista', 'Turista'),
        ('Premiun', 'Premium')
    )
    ESTADO_OPCIONES = (
        ('Disponible', 'Disponible'),
        ('No disponible', 'No disponible'),
    )
    UBICACION_OPCIONES = (
        ('Norponiente', 'Norponiente'),
        ('Nororiente', 'Nororiente'),
        ('Surponiente', 'Surponiente'),
        ('Suroriente', 'Suroriente'),
    )
    numero = models.IntegerField()
    descripción = models.TextField()
    precio = models.IntegerField()
    categoria = models.CharField(max_length=20, choices=HAB_CATEGORIA)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES)
    ubicacion = models.CharField(max_length=20, choices=UBICACION_OPCIONES)
    imagen_1 = models.ImageField(upload_to='habitaciones', blank=True, null=True)
    imagen_2 = models.ImageField(upload_to='habitaciones', blank=True, null=True)
    imagen_3 = models.ImageField(upload_to='habitaciones', blank=True, null=True)

    def __str__(self):
        campos = [f"{field.name}: {getattr(self, field.name)}" for field in self._meta.fields if getattr(self, field.name) != "" and getattr(self, field.name) != None]
        return ", ".join(campos)

#Tabla Reservas
class Reservas(models.Model):
    ESTADO_RESERVAS = (
        ('Confirmada', 'Confirmada'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada'),
    )
    ESTADO_PAGO = (
        ('Pendiente', 'Pendiente'),
        ('Realizado', 'Realizado'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitaciones, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField() #check in llegada
    fecha_fin = models.DateTimeField() #check out salida
    estado = models.CharField(max_length=20, choices=ESTADO_RESERVAS)
    pago = models.CharField(max_length=20, choices=ESTADO_PAGO, default='Pendiente')  # Campo de pago

    def __str__(self):
        return f'{self.user} ha reservado la {self.habitacion} desde {self.fecha_inicio} hasta {self.fecha_fin}'
