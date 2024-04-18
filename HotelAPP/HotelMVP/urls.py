from django.urls import path
from .views import ReservasLista, HabitacionesLista
app_name='HotelMVP'

urlpatterns = [
    path('habitaciones_list/', HabitacionesLista.as_view(), name='HabitacionesLista'),
    path('reservas_list/', ReservasLista.as_view(), name='ReservasLista'),
]
