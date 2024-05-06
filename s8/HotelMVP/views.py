from django.shortcuts import (
    render,
    HttpResponse,
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
)
from django.views import View
from django.views.generic import TemplateView, ListView, FormView
from .models import Habitaciones, Reservas, CustomUser
from .forms import DisponibilidadForm, ReservaForm, BancoForm, RegistroForm
from HotelMVP.reservas_funciones.disponibilidad import revisar_disponibilidad
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator


class HomePageView(TemplateView):
    template_name = "home.html"


class HabitacionesListaVista(View):
    def get(self, request):
        habitaciones_disponibles = Habitaciones.objects.filter(estado="Disponible")

        habitacion_list = []
        for habitacion in habitaciones_disponibles:
            habitacion_url = reverse(
                "HotelMVP:HabitacionDetallesVista", kwargs={"numero": habitacion.numero}
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

        context = {"habitacion_list": habitacion_list}
        return render(request, "habitaciones_list_view.html", context)


class ReservasLista(ListView):
    model = Reservas
    template_name = "reservas_lista.html"
    context_object_name = "reservas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reserva"] = Reservas.objects.first()
        return context


class HabitacionDetallesVista(View):
    def get(self, request, *args, **kwargs):
        numero = self.kwargs.get("numero", None)
        habitacion = get_object_or_404(Habitaciones, numero=numero)
        form = DisponibilidadForm()
        imagenes = [habitacion.imagen_1, habitacion.imagen_2, habitacion.imagen_3]
        context = {"habitacion": habitacion, "imagenes": imagenes, "form": form}
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

        if disponibilidad_habitaciones:
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
                "Todas las habitaciones de esta categoria están reservadas!! Inténte otra categoria."
            )


@method_decorator(login_required, name="dispatch")
class ModificarReservaView(View):
    def get(self, request, id_reserva):
        reserva = get_object_or_404(Reservas, id=id_reserva)
        form = ReservaForm(instance=reserva)
        return render(
            request, "modificar_reserva.html", {"form": form, "reserva": reserva}
        )

    def post(self, request, id_reserva):
        reserva = get_object_or_404(Reservas, id=id_reserva)
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect(reverse("HotelMVP:ReservasLista"))
        else:
            return render(
                request, "modificar_reserva.html", {"form": form, "reserva": reserva}
            )


@method_decorator(login_required, name="dispatch")
class EliminarReservaView(View):
    def post(self, request, id_reserva):
        reserva = get_object_or_404(Reservas, id=id_reserva)
        reserva.delete()
        return redirect("HotelMVP:ReservasLista")


@method_decorator(login_required, name="dispatch")
class BancoView(View):
    def get(self, request, id_reserva):
        reserva = get_object_or_404(Reservas, id=id_reserva)
        form = BancoForm(instance=reserva)
        return render(request, "banco.html", {"form": form, "reserva": reserva})

    def post(self, request, id_reserva):
        reserva = get_object_or_404(Reservas, id=id_reserva)
        form = BancoForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect(reverse("HotelMVP:ReservasLista"))


class RegistroView(View):
    def get(self, request):
        form = RegistroForm()
        return render(request, "registro.html", {"form": form})

    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("HotelMVP:home")
        else:
            return render(request, "registro.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request, "login.html", {"error_message": "Credenciales inválidas"}
            )
