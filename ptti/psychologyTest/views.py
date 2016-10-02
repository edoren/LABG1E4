# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from ptti.psychologyTest.models import Perfil_admin

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
    return render(request, "home.html", {})