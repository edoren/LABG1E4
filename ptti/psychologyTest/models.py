# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#from django.contrib.auth.models import User

class Perfil_admin(models.Model):
	CAMBIO_DOCUMENTO = (('TI','Tarjeta de Identidad'), ('CC','Cedula de Ciudadania'), ('CE','Cedula de Extranjería'))
	CAMBIO_GENERO = (('M','Masculino'),('F','Femenino'),('O','Lgtbi'))
	CAMBIO_ROL = (('ADMIN','Administrador'),('PSI','Psicólogo'),('EST','Estudiante'))

	#usuario = models.OneToOneField(User, verbose_name="Usuario Administrador")
	tipo_documento = models.CharField(max_length=5, choices = CAMBIO_DOCUMENTO, default='CC', verbose_name="Tipo de documento", blank=False)
	documento = models.CharField(max_length = 25, verbose_name="Documento", blank=False,null=False)
	genero = models.CharField(max_length=2, choices = CAMBIO_GENERO, verbose_name="Género", blank=False)
	primer_nombre = models.CharField(max_length=20, blank=False,null=False)
	segundo_nombre = models.CharField(max_length=20, blank=True,null=True)
	primer_apellido = models.CharField(max_length=20, blank=False,null=False)
	segundo_apellido = models.CharField(max_length=20, blank=True,null=True)
	fecha_nacimiento = models.DateField(null=False, blank=False)
	direccion = models.CharField(max_length=30, blank=False,null=False)
	telefono = models.CharField(max_length=20, blank=False,null=False)

	email = models.EmailField()
	contrasena = models.CharField(max_length=50)
	rol = models.CharField(max_length=5, choices = CAMBIO_ROL, default='ADMIN', verbose_name="Rol", blank=False)

	estado = models.BooleanField(default=False, blank=False)
	creado = models.DateTimeField(auto_now_add = True)
	modificado = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return "%s"%(self.email)


class Perfil_estudiante(models.Model):
	CAMBIO_DOCUMENTO = (('TI','Tarjeta de Identidad'), ('CC','Cedula de Ciudadania'), ('CE','Cedula de Extranjería'))
	CAMBIO_GENERO = (('M','Masculino'),('F','Femenino'),('O','Lgtbi'))
	CAMBIO_ROL = (('ADMIN','Administrador'),('PSI','Psicólogo'),('EST','Estudiante'))

	#usuario = models.OneToOneField(User, verbose_name="Usuario Administrador")
	tipo_documento = models.CharField(max_length=5, choices = CAMBIO_DOCUMENTO, default='CC', verbose_name="Tipo de documento", blank=False)
	documento = models.CharField(max_length = 25, verbose_name="Documento", blank=False,null=False)
	genero = models.CharField(max_length=2, choices = CAMBIO_GENERO, verbose_name="Género", blank=False)
	primer_nombre = models.CharField(max_length=20, blank=False,null=False)
	segundo_nombre = models.CharField(max_length=20, blank=True,null=True)
	primer_apellido = models.CharField(max_length=20, blank=False,null=False)
	segundo_apellido = models.CharField(max_length=20, blank=True,null=True)
	fecha_nacimiento = models.DateField(null=False, blank=False)
	direccion = models.CharField(max_length=30, blank=False,null=False)
	telefono = models.CharField(max_length=20, blank=False,null=False)

	email = models.EmailField()
	contrasena = models.CharField(max_length=50)
	grupo = models.CharField(max_length=20, blank=False,null=False)
	institucion = models.CharField(max_length=20, blank=False, null=False)
	rol = models.CharField(max_length=5, choices = CAMBIO_ROL, default='ADMIN', verbose_name="Rol", blank=False)

	estado = models.BooleanField(default=False, blank=False)
	creado = models.DateTimeField(auto_now_add = True)
	modificado = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return "%s"%(self.email)

class Perfil_psicologo(models.Model):
	CAMBIO_DOCUMENTO = (('TI','Tarjeta de Identidad'), ('CC','Cedula de Ciudadania'), ('CE','Cedula de Extranjería'))
	CAMBIO_GENERO = (('M','Masculino'),('F','Femenino'),('O','Lgtbi'))
	CAMBIO_ROL = (('ADMIN','Administrador'),('PSI','Psicólogo'),('EST','Estudiante'))

	#usuario = models.OneToOneField(User, verbose_name="Usuario Administrador")
	tipo_documento = models.CharField(max_length=5, choices = CAMBIO_DOCUMENTO, default='CC', verbose_name="Tipo de documento", blank=False)
	documento = models.CharField(max_length = 25, verbose_name="Documento", blank=False,null=False)
	genero = models.CharField(max_length=2, choices = CAMBIO_GENERO, verbose_name="Género", blank=False)
	primer_nombre = models.CharField(max_length=20, blank=False,null=False)
	segundo_nombre = models.CharField(max_length=20, blank=True,null=True)
	primer_apellido = models.CharField(max_length=20, blank=False,null=False)
	segundo_apellido = models.CharField(max_length=20, blank=True,null=True)
	fecha_nacimiento = models.DateField(null=False, blank=False)
	direccion = models.CharField(max_length=30, blank=False,null=False)
	telefono = models.CharField(max_length=20, blank=False,null=False)

	email = models.EmailField()
	contrasena = models.CharField(max_length=50)

	rol = models.CharField(max_length=5, choices = CAMBIO_ROL, default='ADMIN', verbose_name="Rol", blank=False)

	estado = models.BooleanField(default=False, blank=False)
	creado = models.DateTimeField(auto_now_add = True)
	modificado = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return "%s"%(self.email)

class institucion(models.Model):
	nit = models.CharField(max_length = 15, verbose_name="Nit", blank=False,null=False)
	nombre = models.CharField(max_length=30, blank=False,null=False)
	direccion = models.CharField(max_length=30, blank=False,null=False)
	ciudad = models.CharField(max_length=30, blank=False,null=False)
	telefono = models.CharField(max_length=20, blank=False,null=False)
	sitio_web = models.CharField(max_length=30, blank=False,null=False)

	creado = models.DateTimeField(auto_now_add = True)
	modificado = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return "%s"%(self.nombre)

class grupo(models.Model):
	nombre = models.CharField(max_length=30, blank=False,null=False)
	grado = models.CharField(max_length=15, blank=False,null=False)
	jornada = models.CharField(max_length=30, blank=False,null=False)

	creado = models.DateTimeField(auto_now_add = True)
	modificado = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return "%s"%(self.nombre)