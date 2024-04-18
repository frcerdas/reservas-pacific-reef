from django.shortcuts import render
from .models import Habitaciones, Reservas
from django.views.generic import ListView

# Create your views here.
class HabitacionesLista(ListView):
    model = Habitaciones

class ReservasLista(ListView):
    model = Reservas