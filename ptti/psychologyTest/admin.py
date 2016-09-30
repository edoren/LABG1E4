# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Perfil_admin, Perfil_estudiante, Perfil_psicologo, institucion, grupo

class ProfileAdmin(admin.ModelAdmin):

    list_display =["tipo_documento","documento","genero","primer_nombre","segundo_nombre","primer_apellido","segundo_apellido","fecha_nacimiento","direccion","telefono","email","contrasena","rol","estado","creado","modificado"]
    class Meta:
        model = Perfil_admin


admin.site.register(Perfil_admin, ProfileAdmin)

class ProfileAdminEstudiante(admin.ModelAdmin):

    list_display =["tipo_documento","documento","genero","primer_nombre","segundo_nombre","primer_apellido","segundo_apellido","fecha_nacimiento","direccion","telefono","email","contrasena","grupo","institucion","rol","estado","creado","modificado"]
    class Meta:
        model = Perfil_estudiante


admin.site.register(Perfil_estudiante, ProfileAdminEstudiante)

class ProfileAdminPsicologo(admin.ModelAdmin):

    list_display =["tipo_documento","documento","genero","primer_nombre","segundo_nombre","primer_apellido","segundo_apellido","fecha_nacimiento","direccion","telefono","email","contrasena","rol","estado","creado","modificado"]
    class Meta:
        model = Perfil_psicologo


admin.site.register(Perfil_psicologo, ProfileAdminPsicologo)

class ProfileAdminInstutucion(admin.ModelAdmin):

    list_display =["nit","nombre","direccion","ciudad","telefono","sitio_web","creado","modificado"]
    class Meta:
        model = institucion


admin.site.register(institucion, ProfileAdminInstutucion)

class ProfileAdminGrupo(admin.ModelAdmin):

    list_display =["nombre","grado","jornada","creado","modificado"]
    class Meta:
        model = grupo


admin.site.register(grupo, ProfileAdminGrupo)