# -*- coding:utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import Perfil_usuario, Institucion, Admin, Grupo, Grupo_institucion, Estudiante, Psicologo

CAMBIO_DOCUMENTO = (('TI','Tarjeta de Identidad'), ('CC','Cedula de Ciudadania'), ('CE','Cedula de Extranjería'))
CAMBIO_GENERO = (('M','Masculino'),('F','Femenino'),('O','Lgtbi'))
CAMBIO_ROL = (('ADMIN','Administrador'),('PSI','Psicólogo'),('EST','Estudiante'))


class addPerfil_usuarioForms(ModelForm):

    class Meta:
        model = Perfil_usuario
        fields = [
            "tipo_documento",
            "Nro_dodocumento",
            "genero",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "fecha_nacimiento",
            "direccion",
            "telefono",
            "email",
            "contrasena",
            "rol",
            "estado_activo"
        ]

	DATEPICKER = {
        'type': 'text',
        'class': 'form-control',
        'id': 'datetimepicker4'
    }

	tipo_documento = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=CAMBIO_DOCUMENTO)####
	Nro_dodocumento = forms.CharField(required=True, label='Número de documento',  widget= forms.TextInput(attrs={'size': 25, 'title': 'Número de documento',}))#
	genero = forms.ChoiceField(required=True,widget=forms.Select,choices=CAMBIO_GENERO)#
	primer_nombre = forms.CharField(required=True, label='Primer Nombre', widget= forms.TextInput(attrs={'size': 20, 'title': 'Primer Nombre',}))#
	segundo_nombre = forms.CharField(required=False, label='Segundo Nombre', widget= forms.TextInput(attrs={'size': 20, 'title': 'Segundo Nombre',}))#
	primer_apellido = forms.CharField(required=True, label='Primer Apellido', widget= forms.TextInput(attrs={'size': 20, 'title': 'Primer Apellido',}))#
	segundo_apellido = forms.CharField(required=False, label='Segundo Nombre', widget= forms.TextInput(attrs={'size': 20, 'title': 'Segundo Nombre',}))#
	fecha_nacimiento = forms.DateField(required=True, label='Fecha de nacimiento', widget=forms.DateInput(attrs=DATEPICKER))#
	direccion = forms.CharField(required=True, label='Dirección de Residencia', widget= forms.TextInput(attrs={'size': 30, 'title': 'Dirección de Residencia',}))#
	telefono = forms.CharField(required=True, label='Número de teléfono', widget= forms.TextInput(attrs={'size': 20, 'title': 'Número de teléfono',}))#

	email = forms.EmailField(required=True, label='Email', widget=forms.TextInput())#
	contrasena = forms.CharField(required=True, label='Contraseña', widget=forms.PasswordInput(render_value=False))#
	rol = forms.ChoiceField(required=True,widget=forms.Select,choices=CAMBIO_ROL)#
	estado_activo = forms.BooleanField( required=True)

	# def clean(self):
	# 	return self.cleaned_data

class addInstitucionForms(forms.Form):
	nit = forms.CharField(required=True, label='Número de Nit',  widget= forms.TextInput(attrs={'size': 20, 'title': 'Número de Nit',}))#
#	usuario = models.ForeignKey(Perfil_usuario, verbose_name="Usuario")
	#usuario = forms.ForeignKey(Perfil_usuario)

	nombre = forms.CharField(required=True, label='Nombre instutución', widget= forms.TextInput(attrs={'size': 30, 'title': 'Nombre instutución',}))#
	direccion = forms.CharField(required=True, label='Dirección de la institución', widget= forms.TextInput(attrs={'size': 30, 'title': 'Dirección de la institución',}))#
	ciudad = forms.CharField(required=True, label='Cuidad', widget= forms.TextInput(attrs={'size': 30, 'title': 'Cuidad',}))#
	telefono = forms.CharField(required=True, label='Número de teléfono', widget= forms.TextInput(attrs={'size': 20, 'title': 'Número de teléfono',}))#
	sitio_web = forms.URLField(required=True, label='Sitio Web')#

	estado_activo = forms.BooleanField( required=True)

class addAdminForms(forms.Form):
   # usuario = models.ForeignKey(Perfil_usuario, verbose_name="Usuario")
   # institucion  = models.ForeignKey(Institucion)

    estado_activo = forms.BooleanField( required=True)

class addGrupoForms(forms.Form):
	#usuario = models.ForeignKey(Perfil_usuario, verbose_name="Usuario")
	nombre = forms.CharField(required=True, label='Nombre del Grupo', widget= forms.TextInput(attrs={'size': 30, 'title': 'Nombre del Grupo',}))#
	grado = forms.CharField(required=True, label='Grado del Grupo', widget= forms.TextInput(attrs={'size': 30, 'title': 'Grado del Grupo',}))#
	jornada = forms.CharField(required=True, label='Jornada del Grupo', widget= forms.TextInput(attrs={'size': 30, 'title': 'Jornada del Grupo',}))#

	estado_activo = forms.BooleanField( required=True)

class addGrupo_institucionFomrs(forms.Form):
	#grupo  = models.ForeignKey(Grupo)
	#usuario = models.ForeignKey(Perfil_usuario, verbose_name="Usuario")
	#institucion  = models.ForeignKey(Institucion)

	estado_activo = forms.BooleanField( required=True)

class addEstudianteForms(forms.Form):
	#grupo  = models.ForeignKey(Grupo)
	#usuario = models.ForeignKey(Perfil_usuario, verbose_name="Usuario")

	estado_activo = forms.BooleanField( required=True)

class addPsicologoForms(forms.Form):
	#grupo  = models.ForeignKey(Grupo)
	#usuario = models.ForeignKey(Perfil_usuario, verbose_name="Usuario")

	estado_activo = forms.BooleanField( required=True)

