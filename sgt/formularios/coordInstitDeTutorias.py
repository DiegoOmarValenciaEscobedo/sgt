from django import forms
from sgt.models import Departamento

TIPODEPERIODO = (
    ('1', 'Invierno'),
    ('2', 'Otoño'),
    ('3', 'Verano'),
)

class crearPeriodo(forms.Form):
    tipo = forms.ChoiceField(
        label='Tipo de periodo',
        widget= forms.Select(attrs={
            'class':'form-control'
        }),
        choices=TIPODEPERIODO,
    )

    fechaInicio = forms.DateField(
        label='Fecha de inicio',
        widget=forms.DateInput(attrs={
            'class':'form-control', 'type':'date', 'min':'2022-01-01', 'max':'2100-01-01'
        })
    )

    fechaFin = forms.DateField(
        label='Fecha de fin',
        widget=forms.DateInput(attrs={
            'class':'form-control', 'type':'date', 'min':'2022-01-01', 'max':'2100-01-01'
        })
    )

class crearCarrera(forms.Form):
    nombre = forms.CharField(
        max_length=75,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingresa el nombre de la carrera', 'class':'form-control',
            }
        )
    )
    departamento = forms.ModelChoiceField(
        label='departamento',
        queryset=Departamento.objects.all().values_list('nombre', flat=True).order_by('id'),
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        )   
    )
    nomenclatura = forms.CharField(
        max_length=3,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingresa la nomenclatura de la carrera', 'class':'form-control',
            }
        )
    )

class crearDepartamento(forms.Form):
    nombre = forms.CharField(
        max_length=75,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingresa el nombre del departamento', 'class':'form-control',
            }
        )
    )