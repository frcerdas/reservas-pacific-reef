from django.db import models

# Create your models here.
class Usuarios(models.Model):
    ROLES_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Trabajador', 'Trabajador'),
        ('Huésped', 'Huésped'),
    ]
    nombre = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    contraseña = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROLES_CHOICES)
