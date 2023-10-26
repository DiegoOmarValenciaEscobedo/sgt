from dataclasses import fields
from logging import PlaceHolder
from secrets import choice
from tkinter import Place
from tkinter.ttk import Style
from django.forms.widgets import NumberInput
from tokenize import group
from django import forms

from sgt.models import ESTADO, MyUser, Grupo, Personal_Carrera, Departamento, Citas, Periodo, Carrera, Personal, Reportes

GROUP_TUTOR =[]
grupos = Grupo.objects.all()
for a in grupos:
    GROUP_TUTOR.append([a.id, a.nombre])

class AgregarQuejaSugerencia(forms.Form):
    hint = forms.CharField(
        label="Escribe aquí tu sugerencia",
        max_length=200,
        widget=forms.Textarea(
            attrs={'placeholder': 'Escribe aquí tu sugerencia', 'class': 'w-100 rounded-5',
                    'style': 'resize: none; font-size: 20px; border-radius: 10px;', 'cols': '20', 'rows': '5'}
        )
    )

class TutoradoFirstLogin(forms.Form):
    nombre = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu nombre', 'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important',
            }
        )
    )
    aPaterno = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu apellido paterno', 'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important',
            }
        )
    )
    aMaterno = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu apellido materno', 'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important',
            }
        )
    )
    GENEROS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('NB', 'No Binario'),
    )
    genero = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important', 
        }),
        choices=GENEROS,
    )
    telefono = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu número telefónico', 'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important',
            }
        )
    )
    fechaDeNacimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important', 'type':'date', 'min':'1899-01-01', 'max':'2000-13-13'
            }
        )
    )
    curp = forms.CharField(
        max_length=18,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu CURP', 'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important',
            }
        )
    )
    ESTADOCIVIL = (
        ('SO', 'Soltero'),
        ('CA', 'Casado'),
    )
    estadoCivil = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important', 
        }),
        choices=ESTADOCIVIL,
    )
    nss = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu número de servicio médico', 'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important',
            }
        )
    )
    ENTIDADES = (
        ('AGU', 'Aguascalientes'),
        ('BCN', 'Baja California'),
        ('BCS', 'Baja California Sur'),
        ('CAM', 'Campeche'),
        ('CHP', 'Chiapas'),
        ('CHH', 'Chihuahua'),
        ('COA', 'Coahuila'),
        ('COL', 'Colima'),
        ('DIF', 'Distrito Federal'),
        ('DUR', 'Durango'),
        ('GUA', 'Guanajuato'),
        ('GRO', 'Guerrero'),
        ('HID', 'Hidalgo'),
        ('JAL', 'Jalisco'),
        ('MIC', 'Michoacán'),
        ('MOR', 'Morelos'),
        ('MEX', 'Estado de México'),
        ('NAY', 'Nayarit'),
        ('NLE', 'Nuevo León'),
        ('OAX', 'Oaxaca'),
        ('PUE', 'Puebla'),
        ('QUE', 'Querétaro'),
        ('ROO', 'Quintana Roo'),
        ('SLP', 'San Luis Potosí'),
        ('SIN', 'Sinaloa'),
        ('SON', 'Sonora'),
        ('TAB', 'Tabasco'),
        ('TAM', 'Tamaulipas'),
        ('TIA', 'Tlaxcala'),
        ('VER', 'Veracruz'),
        ('YUC', 'Yucatán'),
        ('ZAC', 'Zacatecas'),
    )
    entidadFed = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important', 
        }),
        choices=ENTIDADES,
    )
    municipio = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu municipio', 'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important',
            }
        )
    )
    domicilio = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu domicilio (calle y número)', 'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important',
            }
        )
    )
    cp = forms.CharField(
        max_length=5,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu código postal', 'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important',
            }
        )
    )
    contactConfianza = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tu contacto de confianza', 'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important',
            }
        )
    )
    termycond = forms.BooleanField()

class cambiarFoto(forms.ModelForm):
    fotoDePerfil = forms.ImageField(label='')
    fotoDePerfil.widget.attrs.update({'onchange': 'resizeImage();', 'style': 'margin: auto !important;', 'id': 'imagenSubida'})

    class Meta:
        model = MyUser
        fields = ['fotoDePerfil']

class verDatosSolcitante(forms.Form):
    motivos = forms.CharField(
        label="listaMotivos",
        widget=forms.Textarea(
            attrs={'style': 'resize: none; font-size: 16px; border-radius: 10px;',
                    'cols': '20', 'rows': '2', 'readonly':'', 'class': 'form-control'}
        )
    )

    descripcion = forms.CharField(
        label="descripcionSolicitante",
        widget=forms.Textarea(
            attrs={'style': 'resize: none; font-size: 16px; border-radius: 10px;',
                    'cols': '20', 'rows': '4', 'readonly':'', 'class': 'form-control'}
        )
    )

class agendarCitaPsicologo(forms.Form):  

    idCita = forms.CharField(
        widget= forms.HiddenInput(
            attrs={'value':'{{citaNueva.id}}', 'name':'{{citaNueva.id}}'}
        )
    )

    fecha = forms.DateField(
        label="Fecha",        
        required=True,  
        widget=NumberInput(
            attrs={'class': 'form-control datepicker-input date', 'type':'date', 'required':'', 'name':'fechaAgenda'})
    )
    descripcion = forms.CharField(
        label="Descripción",
        max_length=200,     
        required=True,   
        widget=forms.Textarea(
            attrs={'placeholder': 'Agrega una descripción aquí', 'style': 'resize: none; font-size: 16px; border-radius: 10px;',
                    'cols': '20', 'rows': '4', 'required':'', 'class': 'form-control','name':'descAgenda'}
        )
    )

MOTIVE_CHOICES =(
    ("1", "Tristeza profunda o constante"),
    ("2", "Angustia"),
    ("3", "Ansiedad"),
    ("4", "Desesperación constante"),
    ("5", "Llanto súbito o continuo"),
    ("6", "Cambios bruscos de conducta"),
    ("7", "Cambios súbitos de estado de animo"),
    ("8", "Excitación o alteración psicomotriz"),
    ("9", "Irritabilidad constante sin motivo aparente"),
    ("10", "Consumo de drogas"),
    ("11", "Dificultades severas de aprendizaje"),
    ("12", "Auto agresiones"),
    ("13", "Otro"),
)        

class CreateDate(forms.Form):
    motive = forms.MultipleChoiceField(
        choices = MOTIVE_CHOICES,
        widget = forms.SelectMultiple(
            attrs={'class': 'form-control motivos', 
            'style': 'width: 100% !important; font-size: 2vh;'}
        )
    )

    description = forms.CharField(
        max_length = 200,
        widget = forms.Textarea(
            attrs={'placeholder':'Describa el motivo','class': 'w-100 rounded-5', 'required':'true', 
            'style':'resize: none; font-size: 2vh; border-radius: 10px;', 'cols':'30', 'rows':'5;'}
        )
        )
    date = forms.CharField(
        widget= forms.DateInput(
            format='%YYYY-%MM-%DD',
            attrs={
                'class': 'form-control date', 'type': 'date',
            'data-target': '#datetimepicker1', 'style': 'width: 100%; border-radius: 10px; font-size: calc(8px + 0.390625vw); border: 2px solid lightgray;'
            }
        )
        )

class AssignGroup(forms.Form):
    grp = forms.ChoiceField(
        choices=GROUP_TUTOR,
        widget = forms.Select(
            attrs={'class': 'form-control', 
            'style': 'width: 100% !important; font-size: 15px'}
        )
    )

class CreateActivity(forms.Form):
    date = forms.CharField(
        widget= forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control date', 'type': 'date',
            'data-target': '#datetimepicker1', 'style': 'width: 100%; border-radius: 10px; font-size: calc(8px + 0.390625vw); border: 2px solid lightgray;'
            }
        )
    )
    tittle = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Agrega un título', 'class': 'form-control-plaintext', 'style': 'border: 2px solid lightgray; border-radius: 10px; font-size: calc(11px + 0.390625vw);'
            }
        )
    )
    description = forms.CharField(
        max_length = 400,
        widget = forms.Textarea(
            attrs={'placeholder':'Describa la actividad','class': 'w-100 rounded-5', 
            'style':'resize: none; font-size: calc(12px + 0.390625vw); border-radius: 10px; border: 2px solid lightgray;', 'cols':'30', 'rows':'5;'}
        )
        )
    fileLoad = forms.FileField(
        widget = forms.FileInput(
            attrs={
                'class': 'form-control form-control-md', 'id': 'formFileSm', 'style': 'font-size: calc(10px + 0.390625vw); border: 2px solid lightgray; border-radius: 10px;'
            }
        )
    )

class CambiarPassword(forms.Form):
    actual = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class':'col-sm-6 p-1'
            }
        )
    )
    nueva = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class':'col-sm-6 p-1'
            }
        )
    )
    repetirNueva = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class':'col-sm-6 p-1'
            }
        )
    )

class enviarTarea(forms.Form):
    fileLoad = forms.FileField(
        widget = forms.FileInput(
            attrs={
                'class': 'form-control form-control-md ', 'id': 'formFileSm', 'style': 'font-size: 10px; border: 2px solid lightgray; border-radius: 10px;'
            }
        )
    )

class CreditosComplementarios_tutorado(forms.Form):
    fileLoad = forms.FileField(
        widget = forms.FileInput(
            attrs={
                'class': 'form-control form-control-md ', 'id': 'formFileSm', 'style': 'font-size: 10px; border: 2px solid lightgray; border-radius: 10px;'
            }
        )
    )

    folio = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-md p-0', 'id': 'formTextSm', 'style': 'font-size: 12px; border: 2px solid lightgray; border-radius: 5px;', 'placeholder':'Ingresa el folio'
            }
        )
    )

    fieldDiferenciarCancelar = forms.CharField(        
        widget = forms.HiddenInput(
            attrs={
                'value':'cancelar', 'name':'fieldDiferenciar', 'id':'fieldDiferenciar'
            }
        ),
        required=False
    )
    
    fieldDiferenciarNuevo = forms.CharField(        
        widget = forms.HiddenInput(
            attrs={
                'value':'nuevo', 'name':'fieldDiferenciar', 'id':'fieldDiferenciar'
            }
        ),
        required=False
    )

class ReporteSemestral(forms.Form):
    noControl = forms.CharField(
        required=True,
        max_length= 10,
         widget = forms.TextInput(
            attrs={
                'class': 'form-control obs', 'style': 'font-size: 12px;', 'readonly': ''
            }
        )
    )
    nombre = forms.CharField(
        required=True,
        max_length= 50,
         widget = forms.TextInput(
            attrs={
                'class': 'form-control obs', 'style': 'font-size: 12px;', 'readonly': ''
            }
        )
    )
    tutoriaGrupal = forms.IntegerField(
        required=True,
         widget = forms.NumberInput(
            attrs={
                'class': 'form-control tutoGrupal', 'style': 'font-size: 12px;', 'min': '0', 'max': '16'
            }
        )
    )
    tutoriaIndividual = forms.IntegerField(
        required=True,
         widget = forms.NumberInput(
            attrs={
                'class': 'form-control tutoInd', 'style': 'font-size: 12px;', 'min': '0', 'max': '999'
            }
        )
    )
    estudiantes = forms.IntegerField(
        required=True,
         widget = forms.NumberInput(
            attrs={
                'class': 'form-control estudiantes', 'style': 'font-size: 12px;', 'min': '0', 'max': '999'
            }
        )
    )
    observaciones = forms.CharField(
        required=True,
        max_length= 100,
         widget = forms.TextInput(
            attrs={
                'class': 'form-control obs', 'style': 'font-size: 12px;'
            }
        )
    )
    porcentaje = forms.IntegerField(
        required=True,
         widget = forms.NumberInput(
            attrs={
                'class': 'form-control porcen', 'style': 'font-size: 12px;', 'min': '0', 'max': '100'
            }
        )
    )

class ReporteJDA(forms.Form):
    tutoriaGrupal = forms.CharField(
        max_length= 3,
         widget = forms.NumberInput(
            attrs={
                'class': 'form-control', 'style': 'font-size: 12px;', 'min': '0', 'max': '16'
            }
        )
    )
    tutoriaIndividual = forms.CharField(
        max_length= 3,
         widget = forms.NumberInput(
            attrs={
                'class': 'form-control', 'style': 'font-size: 12px;', 'min': '0', 'max': '999'
            }
        )
    )
    estudiantes = forms.CharField(
        max_length= 3,
         widget = forms.NumberInput(
            attrs={
                'class': 'form-control', 'style': 'font-size: 12px;', 'min': '0', 'max': '999'
            }
        )
    )
    observaciones = forms.CharField(
        max_length= 50,
         widget = forms.TextInput(
            attrs={
                'class': 'form-control', 'style': 'font-size: 12px;'
            }
        )
    )

class gruposDisponibles(forms.Form):
    def __init__(self, *args, **kwargs):
        
        self.user = kwargs.pop('user')
        super(gruposDisponibles, self).__init__(*args, **kwargs)
        self.fields['grupos'].queryset = Personal_Carrera.objects.filter(personal_id__isnull =True,carrera__departamento_id = self.user.personal.departamento_id).select_related('grupo','carrera').values_list('grupo__nombre', flat=True)

    grupos = forms.ModelChoiceField(
        label='grupos',
        queryset=None,
        widget= forms.Select(
            attrs={
                'class':'form-control'
            }
        )
    )

class editTutor(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance')
        super(editTutor, self).__init__(*args, **kwargs)
        self.fields['Nombre'].widget.attrs.update({'value': self.user.nombre})
        self.fields['AP'].widget.attrs.update({'value': self.user.aPaterno})
        self.fields['AM'].widget.attrs.update({'value': self.user.aMaterno})
        self.fields['RFC'].widget.attrs.update({'value': self.user.idTec})
        self.fields['Correo'].widget.attrs.update({'value': self.user.email})
        self.fields['genero'].initial = self.user.genero
        self.fields['Departamento'].initial = self.user.personal.departamento_id
        self.fields['Telefono'].widget.attrs.update({'value': self.user.telefono})
        self.fields['Cubiculo'].widget.attrs.update({'value': self.user.personal.localizacion})
        self.fields['Contrasenia'].widget.attrs.update({'value': ""})

    Nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    AP = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    AM = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    RFC = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Correo = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    departamentos = Departamento.objects.all()
    Departamento = forms.ChoiceField(
        widget=forms.Select(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            },
        ),
        choices = [(d.id, str(d.nombre)) for d in departamentos]
    )
    Telefono = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Cubiculo = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Contrasenia = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            'title':'Dejar en blanco en caso de no querer cambiarla','class': 'form-control col-sm-6', 'style': 'font-size: 12px;', 'PlaceHolder':'Introduzca una nueva contraseña'
            }
        ),
        required = False
    )
    GENEROS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('NB', 'No Binario'),
    )
    genero = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class':'col-sm-12 p-1', 'style': 'margin-top: 0px !important', 
        }),
        choices=GENEROS,
    )


class editTutorado(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance')
        super(editTutorado, self).__init__(*args, **kwargs)
        self.fields['Nombre'].widget.attrs.update({'value': self.user.user.nombre})
        self.fields['AP'].widget.attrs.update({'value': self.user.user.aPaterno})
        self.fields['AM'].widget.attrs.update({'value': self.user.user.aMaterno})
        self.fields['Curp'].widget.attrs.update({'value': self.user.curp})
        self.fields['Correo'].widget.attrs.update({'value': self.user.user.email})
        self.fields['Telefono'].widget.attrs.update({'value': self.user.user.telefono})
        self.fields['Contrasenia'].widget.attrs.update({'value': ""})
        self.fields['NumeroSS'].widget.attrs.update({'value': self.user.nss})
        self.fields['NoControl'].widget.attrs.update({'value': self.user.user.idTec})
        self.fields['Municipio'].widget.attrs.update({'value': self.user.municipio})
        self.fields['Domicilio'].widget.attrs.update({'value': self.user.domicilio})
        self.fields['CP'].widget.attrs.update({'value': self.user.cp})
        self.fields['CC'].widget.attrs.update({'value': self.user.contactConfianza})
        self.fields['Semestre'].widget.attrs.update({'value': self.user.semestre})
        self.fields['genero'].initial = self.user.user.genero
        self.fields['entidadFed'].initial = self.user.entidadFed
        self.fields['estadoCivil'].initial = self.user.estadoCivil
        self.fields['carrera'].initial = self.user.carrera_id
        self.fields['estatus'].initial = self.user.estatus

    Nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    AP = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    AM = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Curp = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    NumeroSS = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    NoControl = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Municipio = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Domicilio = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    CP = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Telefono = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Correo = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    CC = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Contrasenia = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            'title':'Dejar en blanco en caso de no querer cambiarla','class': 'form-control col-sm-6', 'style': 'font-size: 12px;', 'PlaceHolder':'Introduzca una nueva contraseña'
            }
        ),
        required = False
    )
    Semestre = forms.CharField(
        widget=forms.NumberInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;', 'min':'0', 'max':'12'
            }
        )
    )
    GENEROS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('NB', 'No Binario'),
    )
    genero = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class':'form-control col-sm-12 p-1', 'style': 'margin-top: 0px !important', 
        }),
        choices=GENEROS,
    )
    ENTIDADES = (
        ('AGU', 'Aguascalientes'),
        ('BCN', 'Baja California'),
        ('BCS', 'Baja California Sur'),
        ('CAM', 'Campeche'),
        ('CHP', 'Chiapas'),
        ('CHH', 'Chihuahua'),
        ('COA', 'Coahuila'),
        ('COL', 'Colima'),
        ('DIF', 'Distrito Federal'),
        ('DUR', 'Durango'),
        ('GUA', 'Guanajuato'),
        ('GRO', 'Guerrero'),
        ('HID', 'Hidalgo'),
        ('JAL', 'Jalisco'),
        ('MIC', 'Michoacán'),
        ('MOR', 'Morelos'),
        ('MEX', 'Estado de México'),
        ('NAY', 'Nayarit'),
        ('NLE', 'Nuevo León'),
        ('OAX', 'Oaxaca'),
        ('PUE', 'Puebla'),
        ('QUE', 'Querétaro'),
        ('ROO', 'Quintana Roo'),
        ('SLP', 'San Luis Potosí'),
        ('SIN', 'Sinaloa'),
        ('SON', 'Sonora'),
        ('TAB', 'Tabasco'),
        ('TAM', 'Tamaulipas'),
        ('TIA', 'Tlaxcala'),
        ('VER', 'Veracruz'),
        ('YUC', 'Yucatán'),
        ('ZAC', 'Zacatecas'),
    )
    entidadFed = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class':'form-control col-sm-12 p-1', 'style': 'margin-top: 0px !important', 
        }),
        choices=ENTIDADES,
    )
    ESTADOCIVIL = (
        ('SO', 'Soltero'),
        ('CA', 'Casado'),
    )
    estadoCivil = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class':'form-control col-sm-12 p-1', 'style': 'margin-top: 0px !important', 
        }),
        choices=ESTADOCIVIL,
    )
    carreras = Carrera.objects.all()
    #self.fields['Dp'].choices = [(d.id, str(d.nombre)) for d in departamentos]
    carrera = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class':'form-control col-sm-12 p-1', 'style': 'margin-top: 0px !important', 
        }),
        choices=[(d.id, str(d.nombre)) for d in carreras],
    )
    ESTATUS = (
        ('ACT', 'Activo'),
        ('EXP', 'Expulsado'),
    )
    estatus = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class':'form-control col-sm-12 p-1', 'style': 'margin-top: 0px !important', 
        }),
        choices=ESTATUS,
    )


class AddDocente(forms.Form):

    Nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6 ', 'style': 'font-size: 12px;','required':'true'
            }
        )
    )
    AP = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    AM = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    GENEROS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('NB', 'No Binario'),
    )

    Genero = forms.ChoiceField(
        widget=forms.Select(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        ),
        choices = GENEROS
    )
    RFC = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Correo = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;', 'placeholder':'Debe contener dominio @morelia.tecnm.mx'
            }
        )
    )
    Dp = forms.ChoiceField(
        widget=forms.Select(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    users = MyUser.TIPOUSER
    tU = list(users)
    tU.pop(0)
    Tipo = forms.ChoiceField(
        widget=forms.Select(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        ),
        choices=tU
    )
    Telefono = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Cubiculo = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;'
            }
        )
    )
    Contrasenia = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            'class': 'form-control col-sm-6', 'style': 'font-size: 12px;', 'value' : ''
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(AddDocente, self).__init__(*args, **kwargs)
        try:
            departamentos = Departamento.objects.all()
            self.fields['Dp'].choices = [(d.id, str(d.nombre)) for d in departamentos]
        except Exception as e:
            print(e)

class AddAl(forms.Form):
    NoControl = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control', 'style': 'font-size: 12px;', 'with' : '100%'
            }
        )
    )
    Grupo = forms.ChoiceField(
        choices = GROUP_TUTOR,
        widget = forms.Select(
            attrs={
                'class': 'form-control form-control-md p-0', 'id': 'formTextSm', 'style': 'font-size: 12px; border: 2px solid lightgray; border-radius: 5px;', 'placeholder':'Ingresa el folio'
            }
        )
    )

class Eval_Diag(forms.Form):
    Archivo = forms.FileField(
        widget = forms.FileInput(
            attrs={
                'class': 'form-control form-control-md', 'id': 'formFileSm', 'style': 'font-size: 10px; border: 2px solid lightgray; border-radius: 10px;'
            }
        )
    )

    Descripcion = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-md p-0', 'id': 'formTextSm', 'style': 'font-size: 12px; border: 2px solid lightgray; border-radius: 5px;', 'placeholder':'Ingresa la descripción'
            }
        )
    )

    Fecha_de_cierre = forms.CharField(
        widget= forms.DateInput(
            format='%YYYY-%MM-%DD',
            attrs={
                'class': 'form-control date', 'type': 'date',
            'data-target': '#datetimepicker1', 'style': 'width: 100%; border-radius: 10px; font-size: calc(8px + 0.390625vw); border: 2px solid lightgray;'
            }
        )
        )

    Grupo = forms.ChoiceField(
        choices = GROUP_TUTOR,
        widget = forms.Select(
            attrs={
                'class': 'form-control form-control-md p-0', 'id': 'formTextSm', 'style': 'font-size: 12px; border: 2px solid lightgray; border-radius: 5px;', 'placeholder':'Ingresa el folio'
            }
        )
    )

class crearGrupo(forms.Form):

    def __init__(self, *args, **kwargs):
        
        self.user = kwargs.pop('user')
        super(crearGrupo, self).__init__(*args, **kwargs)
        self.fields['carrera'].queryset = Carrera.objects.filter(departamento_id = self.user.personal.departamento.id).values_list('nombre', flat=True)

    carrera = forms.ModelChoiceField(
        label='carrera',
        queryset=None,
        widget= forms.Select(
            attrs={
                'class':'form-control'
            }
        )
    )

    periodo = forms.ModelChoiceField(
        label='periodo',
        queryset=Periodo.objects.all().values_list('fechaInicio', flat=True).order_by('id'),
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        )   
    )

    nombre = forms.CharField(
        label='nombre',
        max_length= 20,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-md'
            }
        )
    )

class RechazarCursoPendiente(forms.Form):
    rechazar = forms.CharField(        
        widget = forms.HiddenInput(
            attrs={
                'value':'{{cursoPendiente.id}}', 'name':'fieldCursoEliminar', 'id':'fieldCursoEliminar'
            }
        ),
        required=False
    )

class AgregarNuevoCurso(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    )

    cantTutorados = forms.CharField(
        label='CantidadTutorados',
        widget=forms.NumberInput(
            attrs={
                'class':'form-control', 'min': '1', 'max': '999',
            }
        )
    )

    folio = forms.CharField(
        label='Folio',
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    )

    valor = forms.CharField(
        label='Valor',
        widget=forms.NumberInput(
            attrs={
                'class':'form-control', 'min': '1', 'max': '2',
            }
        )
    )

    encargadoNombre = forms.ModelChoiceField(
        label='Encargado',
        queryset=Personal.objects.all().select_related('user').values_list('user__idTec', flat=True),
        widget=forms.Select(
            attrs={
                'class':'form-control',
            }
        )
        
    )

class cargarArchivo(forms.Form):
    fileLoad = forms.FileField(
        widget = forms.FileInput(
            attrs={
                'class': 'form-control form-control-md ', 'id': 'formFileSm', 'style': 'font-size: 10px; border: 2px solid lightgray; border-radius: 10px;'
            }
        ),
        label=False
    )