from django.shortcuts import render, HttpResponse
from .models import Habitaciones, Reservas
from django.views.generic import ListView, FormView
from .forms import DisponibilidadForm
from HotelMVP.reservas_funciones.disponibilidad import revisar_disponibilidad

# Create your views here.
class HabitacionesLista(ListView):
    model = Habitaciones

class ReservasLista(ListView):
    model = Reservas

class ReservasVista(FormView):
    form_class = DisponibilidadForm
    template_name = 'disponibilidad_form.html'

    def form_valid(self, form): 
        data = form.cleaned_data
        habitaciones_list = Habitaciones.objects.filter(categoria=data['habitaciones_categoria'])
        disponibilidad_habitaciones = []
        
        for habitacion in habitaciones_list:
            if revisar_disponibilidad(habitacion, data['fecha_inicio'], data['fecha_fin']):
                disponibilidad_habitaciones.append(habitacion)

        if len(disponibilidad_habitaciones) > 0:
            habitacion = disponibilidad_habitaciones[0]
            reservas = Reservas.objects.create(
                user=self.request.user,
                habitacion=habitacion,
                fecha_inicio=data['fecha_inicio'],
                fecha_fin=data['fecha_fin']
            )
            reservas.save()
            return HttpResponse(reservas)
        else:
            return HttpResponse('Todas las habitaciones de esta categoria están reservadas!! Inténte otra categoria')

