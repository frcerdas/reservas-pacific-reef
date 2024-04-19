import datetime
from HotelMVP.models import Habitaciones, Reservas

def revisar_disponibilidad(habitacion, fecha_inicio, fecha_fin):
    disponiblidad_lista=[]
    reservas_list= Reservas.objects.filter(habitacion=habitacion)
    for reservas in reservas_list:
        if reservas.fecha_inicio > fecha_fin or reservas.fecha_fin < fecha_inicio :
            disponiblidad_lista.append(True)
        else:
            disponiblidad_lista.append(False)
    return all(disponiblidad_lista)
