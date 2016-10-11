# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from psychologyTest.models import Perfil_usuario, Institucion, Admin, Grupo, Grupo_institucion, Estudiante, Psicologo

from django.shortcuts import render_to_response
from django.template import RequestContext
from psychologyTest.forms import addPerfil_usuarioForms, addInstitucionForms, addAdminForms, addGrupoForms, addGrupo_institucionFomrs, addEstudianteForms, addPsicologoForms
from django.conf import settings

def login_page(request):
    print "login_page"
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))

    data={}
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username, password
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            if user.is_active:
                print(login(request, user))
                data['success']="login correcto"
                print "success",data
                return HttpResponseRedirect(reverse('home'))
            else:
                data['error']="el usuario no esta activo"
                print "error",data
        else:
            data['error']="Nombre de usuario o contraseña incorrectos"
            print "error",data
    return render(request, "login.html", data)

@login_required(login_url='/')
def logout_page(request):
    print "logout"
    logout(request)
    return HttpResponseRedirect(reverse('login_page'))

@login_required(login_url='/')
def home(request):
    return render(request, "home_admin.html", {})

def register(request):
    return render(request, "register.html", {})

def restore_password(request):
    return render(request, "restore_password.html", {})

@login_required(login_url='/')
def manage_users(request):
    return render(request, "manage_users.html", {})

@login_required(login_url='/')
def manage_groups(request):
    return render(request, "manage_groups.html", {})

@login_required(login_url='/')
def manage_institutions(request):
    return render(request, "manage_institutions.html", {})

@login_required(login_url='/')
def edit_student_profile(request):
    return render(request, "edit_student_profile.html", {})
