from HotelMVP.models import Habitaciones

def get_habitacion_categoria_formato_legible(categoria):
    habitacion = Habitaciones.objects.all()[0]
    habitacion_categoria = dict(Habitaciones.HAB_CATEGORIA).get(categoria, None)
    return habitacion_categoria

#    #habitaciones_list = Habitaciones.objects.filter(categoria=categoria)

    #if len(habitaciones_list) > 0:
    #    habitacion = habitaciones_list [0]
    #    capacidad = habitacion.capacidad
   #     habitacion_categoria = dict(habitacion.HAB_CATEGORIA).get(habitacion.categoria, None)
    #    return habitacion_categoria
   # else:
    #    return None