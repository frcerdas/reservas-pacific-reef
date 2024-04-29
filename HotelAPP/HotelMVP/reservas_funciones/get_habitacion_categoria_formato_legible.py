from HotelMVP.models import Habitaciones

def get_habitacion_categoria_formato_legible(categoria):
    habitacion = Habitaciones.objects.all()[0]
    habitacion_categoria = dict(Habitaciones.HAB_CATEGORIA).get(categoria, None)
    return habitacion_categoria
