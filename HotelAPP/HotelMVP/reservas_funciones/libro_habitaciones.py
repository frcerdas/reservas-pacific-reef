from HotelMVP.models import Reservas, Habitaciones

def libro_habitaciones(request,habitacion, fecha_inicio, fecha_fin):
            #capacidad = habitacion.capacidad
            reserva = Reservas.objects.create(
                user=request.user,
                habitacion=habitacion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            reserva.save()

            return reserva