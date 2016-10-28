# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render, render_to_response
from psychologyTest.forms import (AddGroupForm, AddInstitutionForm,
                                  AddUserForm, EditUserProfileForm)
from psychologyTest.models import Group, Institution, User
from psychologyTest.util import RedirectToHome


def login_page(request):
    data = {}

    if request.user.is_authenticated():
        return RedirectToHome(request.user)

    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            data["error"] = "Nombre de usuario o contraseña incorrectos."
            return render(request, "login.html", data)

        if user.is_active:
            login(request, user)
            data["success"] = "Login correcto"
            return RedirectToHome(user)
        else:
            data["error"] = "El usuario no esta activo o fué eliminado."

    return render(request, "login.html", data)


def register(request):
    return render(request, "register.html", {})


def restore_password(request):
    if request.POST:
        from_email = EMAIL_HOST_USER
        to_email = request.POST.get("email")
        try:
            user = User.objects.get(email=to_email)
        except User.DoesNotExist:
            user = None
        if user is not None:
            password = user.password
            subject = "Alguien solicito reestablecer la contrasena para tu cuenta en PTTI"
            message = "Hola, alguien solicito recientemente que se restablezca tu contrasena de PTTI. Esta es tu contrasena: {}".format(
                password)
            mail = EmailMessage(subject, message, from_email, [to_email])
            mail.send()
        return redirect("login_page")
    else:
        return render(request, "restore_password.html", {})


@login_required(login_url="/")
def logout_page(request):
    logout(request)
    return redirect("login_page")


@login_required(login_url="/")
def home_admin(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    user_profile = User.objects.filter(
        is_active=True).exclude(role="R").exclude(role="A")
    groups = Group.objects.filter(is_active=True)

    if request.method == "POST":
        action = request.POST.get("action")
        print action
        if action == "create":
            form = AddUserForm(request.POST, initial={"is_active": True})
            if form.is_valid():
                usuario = form.save(commit=False)
                usuario.is_active = True
                usuario.save()
            else:
                print form.errors
        elif action == "modify":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                user = User.objects.get(pk=id_obj)
                form = AddUserForm(request.POST, instance=user,
                                   initial={"is_active": True})
                if form.is_valid():
                    usuario = form.save(commit=False)
                    usuario.is_active = True
                    usuario.save()
                else:
                    print form.errors
        elif action == "remove":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                obj = User.objects.get(pk=id_obj)
                obj.is_active = False
                obj.save()

    return render(request, "home_admin.html",
                  {"user_profile": user_profile, "groups": groups})


@login_required(login_url="/")
def home_psychologist(request):
    if request.user.role != "P":
        return RedirectToHome(request.user)

    return render(request, "home_psychologist.html",  {})


@login_required(login_url="/")
def home_student(request):
    if request.user.role != "S":
        return RedirectToHome(request.user)

    return render(request, "home_student.html",  {})


@login_required(login_url="/")
def account_requests(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    return render(request, "account_requests.html", {})


@login_required(login_url="/")
def manage_groups(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    groups = Group.objects.filter(is_active=True)
    institutions = Institution.objects.filter(is_active=True)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            form = AddGroupForm(request.POST)
            if form.is_valid():
                gr = form.save(commit=False)
                gr.is_active = True
                gr.save()
            else:
                print form.errors
        elif action == "modify":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                user = Group.objects.get(pk=id_obj)
                form = AddGroupForm(request.POST, instance=user)
                if form.is_valid():
                    gr = form.save(commit=False)
                    gr.is_active = True
                    gr.save()
                else:
                    print form.errors
        elif action == "remove":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                obj = Group.objects.get(pk=id_obj)
                obj.is_active = False
                obj.save()

    return render(request, "manage_groups.html", {
        "groups": groups,
        "institutions": institutions
    })


@login_required(login_url="/")
def manage_institutions(request):
    if request.user.role != "A":
        return RedirectToHome(request.user)

    institutions = Institution.objects.filter(is_active=True)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            form = AddInstitutionForm(request.POST)
            if form.is_valid():
                inst = form.save(commit=False)
                inst.is_active = True
                inst.save()
            else:
                print form.errors
        elif action == "modify":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                obj = Institution.objects.get(pk=id_obj)
                form = AddInstitutionForm(request.POST, instance=obj)
                if form.is_valid():
                    inst = form.save(commit=False)
                    inst.is_active = True
                    inst.save()
                else:
                    print form.errors
        elif action == "remove":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                obj = Institution.objects.get(pk=id_obj)
                obj.is_active = False
                obj.save()

    return render(request, "manage_institutions.html", {
        "institutions": institutions
    })


@login_required(login_url="/")
def edit_profile(request):
    if request.user.role == "R":
        return RedirectToHome(request.user)

    groups = Group.objects.filter(is_active=True)

    if request.method == "POST":
        form = EditUserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            print form.errors

    BASE = {
        "A": "base_admin.html",
        "P": "base_psychologist.html",
        "S": "base_student.html"
    }

    return render(request, "edit_profile.html", {
        "base": BASE[request.user.role],
        "groups": groups
    })
