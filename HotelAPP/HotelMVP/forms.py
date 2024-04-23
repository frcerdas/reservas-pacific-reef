from django import forms

class DisponibilidadForm (forms.Form):
    fecha_inicio = forms.DateTimeField(required = True, input_formats=['%d/%m/%Y %H:%M'] ) #Fecha checking y hora
    fecha_fin = forms.DateTimeField(required = True, input_formats=['%d/%m/%Y %H:%M'] )  #Fecha checkout y hora



