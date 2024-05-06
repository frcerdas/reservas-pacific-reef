from django.urls import path
from .views import (
    HomePageView,
    ReservasLista,
    HabitacionesListaVista,
    ReservasVista,
    HabitacionDetallesVista,
    ModificarReservaView,
    EliminarReservaView,
    BancoView,
    RegistroView,
    LoginView,
)

app_name = "HotelMVP"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path('login/', LoginView.as_view(), name='login'),
    path("registro/", RegistroView.as_view(), name="registro"),
    path("habitaciones_list/", HabitacionesListaVista.as_view(), name="HabitacionesListaVista"),
    path("reservas_list/", ReservasLista.as_view(), name="ReservasLista"),
    path("disponibilidad_form/", ReservasVista.as_view(), name="ReservasVista"),
    path(
        "habitacion/<str:numero>/",
        HabitacionDetallesVista.as_view(),
        name="HabitacionDetallesVista",
    ),
    path(
        "modificar_reserva/<int:id_reserva>/",
        ModificarReservaView.as_view(),
        name="modificar_reserva",
    ),
    path(
        "eliminar_reserva/<int:id_reserva>/",
        EliminarReservaView.as_view(),
        name="eliminar_reserva"
    ),
    path("banco/<int:id_reserva>/", BancoView.as_view(), name="banco"),
]
