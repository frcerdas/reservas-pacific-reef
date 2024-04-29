import datetime
from HotelMVP.models import Habitaciones, Reservas
from django.utils import timezone  # Importa el módulo de zona horaria de Django

def revisar_disponibilidad(habitacion, fecha_inicio, fecha_fin):
    disponibilidad_lista = []
    reservas_list = Reservas.objects.filter(habitacion=habitacion)
    
    # Convierte las fechas a objetos de zona horaria si es necesario
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)
    
    for reservas in reservas_list:
        # Convierte las fechas de las reservas a objetos de zona horaria si es necesario
        reservas_inicio = reservas.fecha_inicio.replace(tzinfo=timezone.utc)
        reservas_fin = reservas.fecha_fin.replace(tzinfo=timezone.utc)
        
        if reservas_inicio > fecha_fin or reservas_fin < fecha_inicio:
            disponibilidad_lista.append(True)
        else:
            disponibilidad_lista.append(False)
    
    return all(disponibilidad_lista)