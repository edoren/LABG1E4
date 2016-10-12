# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Perfil_usuario, Institucion, Admin, Grupo, Grupo_institucion, Estudiante, Psicologo

class ProfileAdmin(admin.ModelAdmin):

    list_display =["tipo_documento","Nro_dodocumento","genero","primer_nombre","segundo_nombre","primer_apellido","segundo_apellido","fecha_nacimiento","direccion","telefono","email","contrasena","rol","estado_activo","creado","modificado"]
    class Meta:
        model = Perfil_usuario

admin.site.register(Perfil_usuario, ProfileAdmin)

class ProfileAdminInstutucion(admin.ModelAdmin):

    list_display =["nit","nombre","direccion","ciudad","telefono","sitio_web","estado_activo","creado","modificado"]
    class Meta:
        model = Institucion

admin.site.register(Institucion, ProfileAdminInstutucion)

class ProfileAdminAdmin(admin.ModelAdmin):

    list_display =["estado_activo","creado","modificado"]
    class Meta:
        model = Admin

admin.site.register(Admin, ProfileAdminAdmin)

class ProfileAdminGrupo(admin.ModelAdmin):

    list_display =["nombre","grado","jornada","estado_activo","creado","modificado"]
    class Meta:
        model = Grupo

admin.site.register(Grupo, ProfileAdminGrupo)

class ProfileAdminGrupo_institucion(admin.ModelAdmin):

    list_display =["estado_activo","creado","modificado"]
    class Meta:
        model = Grupo_institucion

admin.site.register(Grupo_institucion, ProfileAdminGrupo_institucion)

class ProfileAdminEstudiante(admin.ModelAdmin):

    list_display =["estado_activo","creado","modificado"]
    class Meta:
        model = Estudiante

admin.site.register(Estudiante, ProfileAdminEstudiante)

class ProfileAdminPsicologo(admin.ModelAdmin):

    list_display =["estado_activo","creado","modificado"]
    class Meta:
        model = Psicologo

admin.site.register(Psicologo, ProfileAdminPsicologo)
