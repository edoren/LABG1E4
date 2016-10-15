# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext

from psychologyTest.forms import AddGroupForm, AddInstitutionForm, AddUserForm
from psychologyTest.models import Group, Institution, User
from psychologyTest.private.email import EMAIL_HOST_USER
from psychologyTest.util import RedirectToHome


def login_page(request):
    data = {}

    if request.user.is_authenticated():
        if not isinstance(request.user, User):
            data["error"] = "No tiene una interfaz asignada."
            return render(request, "login.html", data)
        return RedirectToHome(request.user)

    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            data["error"] = "Nombre de usuario o contraseña incorrectos."
            return render(request, "login.html", data)

        if not isinstance(user, User):
            data["error"] = "No tiene permitido acceder por esta interfaz."
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
            message = "Hola, alguien solicito recientemente que se restablezca tu contrasena de PTTI. Esta es tu contrasena: {}".format(password)
            mail = EmailMessage(subject, message, from_email, [to_email])
            mail.send()
        return HttpResponseRedirect(reverse("login_page"))
    else:
        return render(request, "restore_password.html", {})


@login_required(login_url="/")
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse("login_page"))


@login_required(login_url="/")
def home_admin(request):
    if not isinstance(request.user, User) or request.user.role != "A":
        return RedirectToHome(request.user)

    user_profile = User.objects.filter(is_active=True)
    groups = Group.objects.filter(is_active=True)

    if request.method == "POST":
        action = request.POST.get("action")
        print action
        if action == "create":
            form = AddUserForm(request.POST)
            if form.is_valid():
                usuario = form.save(commit=False)
                usuario.is_active = True
                usuario.save()
            else:
                print form.errors
                print "NOT VALID User!!"
        elif action == "modify":
            id_obj = request.POST.get("id")
            if id_obj is not None:
                user = User.objects.get(pk=id_obj)
                form = AddUserForm(request.POST, instance=user)
                if form.is_valid():
                    usuario = form.save(commit=False)
                    usuario.is_active = True
                    usuario.save()
                else:
                    print form.errors
                    print "NOT VALID User!!"
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
    if not isinstance(request.user, User) or request.user.role != "P":
        return RedirectToHome(request.user)

    return render(request, "home_psychologist.html",  {})


@login_required(login_url="/")
def home_student(request):
    if not isinstance(request.user, User) or request.user.role != "S":
        return RedirectToHome(request.user)

    return render(request, "home_student.html",  {})


@login_required(login_url="/")
def account_requests(request):
    if not isinstance(request.user, User) or request.user.role != "A":
        return RedirectToHome(request.user)

    return render(request, "account_requests.html", {})


@login_required(login_url="/")
def manage_groups(request):
    if not isinstance(request.user, User) or request.user.role != "A":
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
    if not isinstance(request.user, User) or request.user.role != "A":
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
def edit_student_profile(request):
    return render(request, "edit_student_profile.html", {})

# @login_required
# def add_dueno(request):
#     if request.method == "POST":
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

#     if request.method == "POST":
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
