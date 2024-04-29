from django import forms
from .models import Reservas    


class DisponibilidadForm(forms.Form):
    fecha_inicio = forms.DateTimeField(
        required=True, input_formats=["%d/%m/%Y %H:%M"]
    )  # Fecha checking y hora
    fecha_fin = forms.DateTimeField(
        required=True, input_formats=["%d/%m/%Y %H:%M"]
    )  # Fecha checkout y hora


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reservas
        fields = ["fecha_inicio", "fecha_fin", "estado", "pago"]

class BancoForm(forms.ModelForm):
    class Meta:
        model = Reservas
        fields = ['pago']