from django import forms

class DisponibilidadForm (forms.Form):
    HAB_CATEGORIA=(
        ('Turista','Turista'),
        ('Premiun','Premiun')
    )
    habitaciones_categoria = forms.ChoiceField(choices=HAB_CATEGORIA, required=True)
    fecha_inicio = forms.DateTimeField(required = True, input_formats=['%d/%m/%Y %H:%M'] ) #Fecha checking y hora
    fecha_fin = forms.DateTimeField(required = True, input_formats=['%d/%m/%Y %H:%M'] )  #Fecha checkout y hora