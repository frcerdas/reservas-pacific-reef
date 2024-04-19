from django.urls import path
from .views import ReservasLista, HabitacionesLista, ReservasVista
app_name='HotelMVP'

urlpatterns = [
    path('habitaciones_list/', HabitacionesLista.as_view(), name='HabitacionesLista'),
    path('reservas_list/', ReservasLista.as_view(), name='ReservasLista'),
    path('disponibilidad_form/',ReservasVista.as_view(), name='ReservasVista'),
]
