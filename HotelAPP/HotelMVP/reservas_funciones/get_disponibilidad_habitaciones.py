from HotelMVP.models import Habitaciones
from .disponibilidad import revisar_disponibilidad
#función que toma categoría y devuelve la lista de habitaciones
def get_disponibilidad_habitaciones(categoria, fecha_inicio, fecha_fin):

    habitaciones_list = Habitaciones.objects.filter(categoria=categoria)

    disponibilidad_habitaciones = []   

    for habitacion in habitaciones_list:
        if revisar_disponibilidad(habitacion, fecha_inicio, fecha_fin):
            disponibilidad_habitaciones.append(habitacion)
    
    if len(disponibilidad_habitaciones) > 0:
        return disponibilidad_habitaciones
    else:
        return None
        