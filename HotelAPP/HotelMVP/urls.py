from django.urls import path
from .views import ReservasListaVista, HabitacionesListaVista, HabitacionDetallesVista, CancelarReservaVista
app_name='HotelMVP'

urlpatterns = [
    path('habitaciones_list/', HabitacionesListaVista, name='HabitacionesListaVista'),
    path('reservas_list/', ReservasListaVista.as_view(), name='ReservasListaVista'),
    path('habitacion/<categoria>',HabitacionDetallesVista.as_view(), name='HabitacionDetallesVista'),
    path('reservas/cancelar/<pk>',CancelarReservaVista.as_view(), name='CancelarReservaVista'),
]
