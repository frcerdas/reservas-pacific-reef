from django.urls import path
from .views import (
    HomePageView,
    ReservasLista,
    HabitacionesListaVista,
    ReservasVista,
    HabitacionDetallesVista, modificar_reserva, eliminar_reserva, banco
)

app_name = "HotelMVP"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("habitaciones_list/", HabitacionesListaVista, name="HabitacionesListaVista"),
    path("reservas_list/", ReservasLista.as_view(), name="ReservasLista"),
    path("disponibilidad_form/", ReservasVista.as_view(), name="ReservasVista"),
    path(
        "habitacion/<str:numero>",
        HabitacionDetallesVista.as_view(),
        name="HabitacionDetallesVista",
    ),
    path("modificar_reserva/<int:id_reserva>/", modificar_reserva, name="modificar_reserva"),
    path('eliminar_reserva/<int:id_reserva>/', eliminar_reserva, name='eliminar_reserva'),
    path('banco/<int:id_reserva>/', banco, name='banco'),
]
