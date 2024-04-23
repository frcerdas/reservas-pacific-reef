from django.urls import path
from .views import ReservasLista, HabitacionesListaVista, ReservasVista, HabitacionDetallesVista
app_name='HotelMVP'

urlpatterns = [
    path('habitaciones_list/', HabitacionesListaVista, name='HabitacionesListaVista'),
    path('reservas_list/', ReservasLista.as_view(), name='ReservasLista'),
    path('disponibilidad_form/',ReservasVista.as_view(), name='ReservasVista'),
    path('habitacion/<categoria>',HabitacionDetallesVista.as_view(), name='HabitacionDetallesVista'),
]
