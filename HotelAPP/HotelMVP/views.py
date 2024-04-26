from django.shortcuts import render, HttpResponse
from .models import Habitaciones, Reservas
from django.views.generic import ListView, FormView, View, DeleteView
from .forms import DisponibilidadForm
from HotelMVP.reservas_funciones.disponibilidad import revisar_disponibilidad
from django.urls import reverse, reverse_lazy
from HotelMVP.reservas_funciones.get_habitacion_cat_url_list import get_habitacion_cat_url_list
from HotelMVP.reservas_funciones.get_habitacion_categoria_formato_legible import get_habitacion_categoria_formato_legible
from HotelMVP.reservas_funciones.get_disponibilidad_habitaciones import get_disponibilidad_habitaciones
from HotelMVP.reservas_funciones.libro_habitaciones import libro_habitaciones
# Create your views here.


def HabitacionesListaVista(request):
    habitacion_categoria_url_list = get_habitacion_cat_url_list()
    # Preparar el contexto con la lista de categorías
    context = {
        'habitacion_list': habitacion_categoria_url_list,
    }

    return render(request, 'habitaciones_list_view.html', context)


class ReservasListaVista(ListView):
    model = Reservas
    template_name ="reservas_list_view.html"
    
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

        habitacion_categoria_formato_legible = get_habitacion_categoria_formato_legible(categoria)

        form = DisponibilidadForm()

        if habitacion_categoria_formato_legible is not None:
            context = {
                'habitaciones_list': habitacion_categoria_formato_legible,
                'capacidad': habitacion_categoria_formato_legible,
                'habitacion_categoria': habitacion_categoria_formato_legible,
                'form': form
            }
            return render(request, 'habitaciones_detalles_view.html', context)

        else:
            return HttpResponse('CATEGORIA NO EXISTE INTENTE OTRA.')

    def post(self, request, *args, **kwargs):

        categoria = self.kwargs.get('categoria', None)

        form = DisponibilidadForm(request.POST)

        habitacion_categoria_formato_legible = get_habitacion_categoria_formato_legible(categoria)
        
        #verifica formato y valida
        if form.is_valid():
            data = form.cleaned_data
            disponibilidad_habitaciones = get_disponibilidad_habitaciones(categoria, data['fecha_inicio'], data['fecha_fin'])

        if disponibilidad_habitaciones is not None:

            reserva = libro_habitaciones(request, disponibilidad_habitaciones[0], data['fecha_inicio'], data['fecha_fin'])

            return HttpResponse(f'Reserva exitosa para la habitación: {reserva.habitacion} desde {reserva.fecha_inicio} hasta {reserva.fecha_fin}')
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
        if disponibilidad_habitaciones:
            return HttpResponse(f'Habitaciones disponibles: {disponibilidad_habitaciones}')
        else:
            return HttpResponse('Todas las habitaciones de esta categoria están reservadas!! Inténte otra categoria')


class CancelarReservaVista(DeleteView):
    template_name= 'reservas_cancelar_view.html'
    model=Reservas
    success_url = reverse_lazy('HotelMVP:ReservasListaVista')
