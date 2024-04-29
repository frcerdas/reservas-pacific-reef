from django.shortcuts import (
    render,
    HttpResponse,
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
)
from .models import Habitaciones, Reservas
from django.views.generic import TemplateView, ListView, FormView, View
from .forms import DisponibilidadForm, ReservaForm, BancoForm
from HotelMVP.reservas_funciones.disponibilidad import revisar_disponibilidad
from django.urls import reverse
from django.db.models import Q

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"


from django.urls import reverse


def HabitacionesListaVista(request):
    habitaciones_disponibles = Habitaciones.objects.filter(estado="Disponible")

    # Crear lista para mantener las habitaciones y sus URLs
    habitacion_list = []
    for habitacion in habitaciones_disponibles:
        # Construir la URL para cada habitación
        habitacion_url = reverse(
            "HotelMVP:HabitacionDetallesVista",
            kwargs={"numero": habitacion.numero},
        )
        habitacion_list.append(
            {
                "habitacion": habitacion,
                "url": habitacion_url,
                "precio": habitacion.precio,
                "numero": habitacion.numero,
                "categoria": habitacion.categoria,
            }
        )

    # Preparar el contexto con la lista de habitaciones
    context = {
        "habitacion_list": habitacion_list,
    }

    return render(request, "habitaciones_list_view.html", context)


class ReservasLista(ListView):
    model = Reservas
    template_name = (
        "reservas_lista.html"  # Nombre del archivo HTML que quieres renderizar
    )
    context_object_name = "reservas"  # Nombre del contexto que se pasará a la plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reserva"] = (
            Reservas.objects.first()
        )  # Aquí selecciona la reserva que quieras pasar al contexto
        return context


class HabitacionDetallesVista(View):
    def get(self, request, *args, **kwargs):
        numero = self.kwargs.get("numero", None)
        habitacion = get_object_or_404(Habitaciones, numero=numero)
        form = DisponibilidadForm()
        imagenes = [habitacion.imagen_1, habitacion.imagen_2, habitacion.imagen_3]
        context = {
            "habitacion": habitacion,
            "imagenes": imagenes,
            "form": form,
        }
        return render(request, "habitaciones_detalles_view.html", context)

    def post(self, request, *args, **kwargs):
        numero = self.kwargs.get("numero", None)
        habitacion = get_object_or_404(Habitaciones, numero=numero)
        form = DisponibilidadForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if revisar_disponibilidad(
                habitacion, data["fecha_inicio"], data["fecha_fin"]
            ):
                reserva = Reservas.objects.create(
                    user=request.user,
                    habitacion=habitacion,
                    fecha_inicio=data["fecha_inicio"],
                    fecha_fin=data["fecha_fin"],
                )
                reserva.save()
                return HttpResponseRedirect(
                    reverse("HotelMVP:banco", kwargs={"id_reserva": reserva.id})
                )
            else:
                return HttpResponse("Habitación reservada. Intente otra fecha.")
        else:
            return HttpResponse("Formulario inválido. Intente nuevamente.")


class ReservasVista(FormView):
    form_class = DisponibilidadForm
    template_name = "disponibilidad_form.html"

    def form_valid(self, form):
        data = form.cleaned_data
        habitaciones_list = Habitaciones.objects.filter(
            categoria=data["habitaciones_categoria"]
        )
        disponibilidad_habitaciones = []

        for habitacion in habitaciones_list:
            if revisar_disponibilidad(
                habitacion, data["fecha_inicio"], data["fecha_fin"]
            ):
                disponibilidad_habitaciones.append(habitacion)

        if len(disponibilidad_habitaciones) > 0:
            habitacion = disponibilidad_habitaciones[0]
            reservas = Reservas.objects.create(
                user=self.request.user,
                habitacion=habitacion,
                fecha_inicio=data["fecha_inicio"],
                fecha_fin=data["fecha_fin"],
            )
            reservas.save()
            return HttpResponse(reservas)
        else:
            return HttpResponse(
                "Todas las habitaciones de esta categoria están reservadas!! Inténte otra categoria"
            )


def modificar_reserva(request, id_reserva):
    reserva = get_object_or_404(Reservas, id=id_reserva)
    if request.method == "POST":
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect(reverse("HotelMVP:ReservasLista"))
    else:
        form = ReservaForm(instance=reserva)
    return render(request, "modificar_reserva.html", {"form": form, "reserva": reserva})


def eliminar_reserva(request, id_reserva):
    reserva = get_object_or_404(Reservas, id=id_reserva)
    if request.method == "POST":
        reserva.delete()
        return redirect("HotelMVP:ReservasLista")
    return redirect("HotelMVP:ReservasLista")


def banco(request, id_reserva):
    reserva = get_object_or_404(Reservas, id=id_reserva)
    if request.method == "POST":
        form = BancoForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect(reverse("HotelMVP:ReservasLista"))
    else:
        form = BancoForm(instance=reserva)
    return render(request, "banco.html", {"form": form, "reserva": reserva})
