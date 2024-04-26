from HotelMVP.models import Habitaciones
from django.urls import reverse
#funcion que de vuelve la lista de habitaciones y su respectiva categoria y categoria url lista habitacion/premiun ejemplo
def get_habitacion_cat_url_list():

    habitacion = Habitaciones.objects.all()[0]
    habitacion_categorias = dict(habitacion.HAB_CATEGORIA)

    # Crear lista para mantener las categorías y sus URLs
    habitacion_cat_url_list = []
    for habitacion_categoria in habitacion_categorias:
        # Construir la URL para cada categoría
        habitacion_url = reverse('HotelMVP:HabitacionDetallesVista', kwargs={'categoria': habitacion_categoria})
        habitacion_cat_url_list.append({'categoria': habitacion_categoria, 'url': habitacion_url, 'descripción': habitacion.descripción, 'precio': habitacion.precio})
    
    return habitacion_cat_url_list