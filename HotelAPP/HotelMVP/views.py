from django.shortcuts import render, HttpResponse
from .models import Habitaciones, Reservas
from django.views.generic import ListView, FormView, View
from .forms import DisponibilidadForm
from HotelMVP.reservas_funciones.disponibilidad import revisar_disponibilidad
from django.urls import reverse
# Create your views here.
def HabitacionesListaVista(request):
    habitacion = Habitaciones.objects.all()[0]
    habitacion_categorias = dict(habitacion.HAB_CATEGORIA)

    # Crear lista para mantener las categorías y sus URLs
    habitacion_list = []
    for habitacion_categoria in habitacion_categorias:
        # Construir la URL para cada categoría
        habitacion_url = reverse('HotelMVP:HabitacionDetallesVista', kwargs={'categoria': habitacion_categoria})
        habitacion_list.append({'categoria': habitacion_categoria, 'url': habitacion_url, 'descripción': habitacion.descripción, 'precio': habitacion.precio})

    # Preparar el contexto con la lista de categorías
    context = {
        'habitacion_list': habitacion_list,
    }

    return render(request, 'habitaciones_list_view.html', context)


class ReservasLista(ListView):
    model = Reservas
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            reservas_list = Reservas.objects.all()
            return reservas_list
        else:
            reservas_list = Reservas.objects.filter(user=self.request.user)
            return reservas_list


class HabitacionDetallesVista(View):
    def get(self, request, *args, **kwargs):
        categoria = self.kwargs.get('categoria', None)
        form = DisponibilidadForm()
        habitaciones_list = Habitaciones.objects.filter(categoria=categoria)
        if len(habitaciones_list) > 0:
            habitacion = habitaciones_list [0]
            capacidad = habitacion.capacidad
            habitacion_categoria = dict(habitacion.HAB_CATEGORIA).get(habitacion.categoria, None)
            context = {
                'habitaciones_list': habitaciones_list,
                'categoria': categoria,
                'capacidad': capacidad,
                'habitacion_categoria': habitacion_categoria,
                'form': form
            }
            return render(request, 'habitaciones_detalles_view.html', context)
        else:
            return HttpResponse('Categoria no existe.')

    def post(self, request, *args, **kwargs):
        categoria = self.kwargs.get('categoria', None)
        habitaciones_list = Habitaciones.objects.filter(categoria=categoria)
        disponibilidad_habitaciones = []
        form = DisponibilidadForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            
        for habitacion in habitaciones_list:
            if revisar_disponibilidad(habitacion, data['fecha_inicio'], data['fecha_fin']):
                disponibilidad_habitaciones.append(habitacion)

        if disponibilidad_habitaciones:
            habitacion = disponibilidad_habitaciones[0]
            capacidad = habitacion.capacidad
            reserva = Reservas.objects.create(
                user=request.user,
                habitacion=habitacion,
                capacidad=capacidad,
                fecha_inicio=data['fecha_inicio'],
                fecha_fin=data['fecha_fin']
            )
            reserva.save()
            return HttpResponse(f'Reserva creada para {reserva.habitacion} desde {reserva.fecha_inicio} hasta {reserva.fecha_fin}')
        else:
            return HttpResponse('Todas las habitaciones de esta categoria están reservadas. Intente otra categoria.')




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

