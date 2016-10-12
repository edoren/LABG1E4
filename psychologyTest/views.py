# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext

from psychologyTest.forms import (addAdminForms, addEstudianteForms,
                                  addGrupo_institucionFomrs, addGrupoForms,
                                  addInstitucionForms, addPerfil_usuarioForms,
                                  addPsicologoForms)
from psychologyTest.models import (Admin, Estudiante, Grupo, Grupo_institucion,
                                   Institucion, Perfil_usuario, Psicologo)

from .forms import addPerfil_usuarioForms


def login_page(request):
    print "login_page"
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("home_student"))

    data = {}
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        print username, password
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            if user.is_active:
                print(login(request, user))
                data["success"] = "login correcto"
                print "success", data
                return HttpResponseRedirect(reverse("home_student"))
            else:
                data["error"] = "el usuario no esta activo"
                print "error", data
        else:
            data["error"] = "Nombre de usuario o contraseña incorrectos"
            print "error", data
    return render(request, "login.html", data)


def register(request):
    return render(request, "register.html", {})  # arreglar


def restore_password(request):
    return render(request, "restore_password.html", {})


@login_required(login_url="/")
def logout_page(request):
    print "logout"
    logout(request)
    return HttpResponseRedirect(reverse("login_page"))


@login_required(login_url="/")
def home_admin(request):
    perfil_usuario = Perfil_usuario.objects.filter(estado_activo=True)

    if request.POST:
        print "es un post"
        form = addPerfil_usuarioForms(request.POST)
        if form.is_valid():
            form.save()
            print "Si es valido"

            # return HttpResponseRedirect("/duenos")
        else:
            print "no es valido"
            print form.errors
    elif request.GET:
        id_obj = request.GET.get("id")
        obj = Perfil_usuario.objects.get(pk=id_obj)
        print obj
    # else:
    #     form = addPerfil_usuarioForms()

    return render(request, "home_admin.html",
                  {"perfil_usuario": perfil_usuario})


@login_required(login_url="/")
def home_psycologist(request):
    return render(request, "home_psycologist.html",  {})


@login_required(login_url="/")
def home_student(request):
    return render(request, "home_student.html",  {})


# # @login_required(login_url="/")
# # def manage_users(request):
#     return render(request, "manage_users.html", {})


@login_required(login_url="/")
def account_requests(request):
    return render(request, "account_requests.html", {})


@login_required(login_url="/")
def manage_groups(request):
    grupo = Grupo.objects.all()
    return render(request, "manage_groups.html", {"grupo": grupo})


@login_required(login_url="/")
def manage_institutions(request):
    institucion = Institucion.objects.all()
    return render(request, "manage_institutions.html",
                  {"institucion": institucion})


@login_required(login_url="/")
def edit_student_profile(request):
    return render(request, "edit_student_profile.html", {})

# @login_required
# def add_dueno(request):
#     if request.POST:
#         form = UsuarioForm(request.POST)
#         if  form.is_valid():
#             usuario = form.save(commit=False)
#             usuario.username = request.POST["documento"]
#             usuario.tipo_usuario = 2
#             usuario.set_password(request.POST["password"])
#             usuario.user_creator = request.user
#             usuario.save()
#             return HttpResponseRedirect("/duenos")
#     else:
#         form = UsuarioForm()
#     return render(request, "add_dueno.html", locals())

# @login_required
# def edit_dueno(request, user_id=None):
#     if user_id:
#         usuario = get_object_or_404(Usuario, pk=user_id, is_active=True)
#         usuario.password = None
#         if usuario.user_creator != request.user:
#             return HttpResponseForbidden()
#     else:
#         return HttpResponseForbidden()

#     if request.POST:
#         form = UsuarioForm(request.POST, instance=usuario)
#         if form.is_valid():
#             usuario.set_password(request.POST["password"])
#             usuario.username = request.POST["documento"]
#             form.save()
#             return HttpResponseRedirect("/duenos")

#     else:
#         form = UsuarioForm(instance=usuario)

#     return render(request, "add_dueno.html", locals())

# @login_required
# def show_dueno(request, user_id):
#     user = get_object_or_404(Usuario, pk = user_id, is_active=True)
#     if user.user_creator != request.user:
#             return HttpResponseForbidden()
#     active_tab = "duenos"
#     return render(request, "show_user.html", locals())

# @login_required
# def delete_dueno(request, user_id):
#     user = get_object_or_404(Usuario, pk = user_id, is_active=True)
#     if user.user_creator != request.user:
#             return HttpResponseForbidden()
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect("/duenos")
