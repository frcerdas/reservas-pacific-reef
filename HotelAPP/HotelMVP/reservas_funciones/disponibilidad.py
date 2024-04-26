import datetime
from HotelMVP.models import Habitaciones, Reservas
from django.utils import timezone 

def revisar_disponibilidad(habitacion, fecha_inicio, fecha_fin):
    
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)

    reservas_list = Reservas.objects.filter(habitacion=habitacion)
    for reserva in reservas_list:
        
        reservas_inicio = reserva.fecha_inicio.astimezone(timezone.utc)
        reservas_fin = reserva.fecha_fin.astimezone(timezone.utc)
        
        if reservas_inicio <= fecha_fin and reservas_fin >= fecha_inicio:
            return False  #

    return True  