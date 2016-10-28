# -*- coding:utf-8 -*-
from django import forms
from models import (Institution, Group, User)
from models import (DOCUMENT_OPTIONS, GENDER_OPTIONS,
                    ROLE_OPTIONS, SCHEDULE_OPTIONS)

DATEPICKER = {
    "type": "text",
    "class": "form-control",
    "id": "datetimepicker4"
}


class AddUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "document_type",
            "document_number",
            "email",
            "password",
            "first_name",
            "last_name",
            "birthdate",
            "gender",
            "address",
            "phone",
            "role",
            # "group",
            "is_active"
        ]

    document_type = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect, choices=DOCUMENT_OPTIONS)
    document_number = forms.CharField(
        required=True, label="Número de documento",
        widget=forms.TextInput(
            attrs={"size": 25, "title": "Número de documento"}))
    gender = forms.ChoiceField(
        required=True, widget=forms.Select, choices=GENDER_OPTIONS)
    first_name = forms.CharField(
        required=True, label="Primer Nombre",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Nombre"}))
    last_name = forms.CharField(
        required=True, label="Apellido",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Apellido"}))
    birthdate = forms.DateField(
        required=True, label="Fecha de nacimiento",
        widget=forms.DateInput(attrs=DATEPICKER))
    address = forms.CharField(
        required=True, label="Dirección de Residencia",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Dirección de Residencia"}))
    phone = forms.CharField(
        required=True, label="Número de teléfono",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Número de teléfono"}))

    email = forms.EmailField(
        required=True, label="Email", widget=forms.TextInput())
    password = forms.CharField(
        required=True, label="Contraseña", widget=forms.PasswordInput())

    role = forms.ChoiceField(
        required=True, widget=forms.Select, choices=ROLE_OPTIONS)

    is_active = forms.BooleanField(required=False)


class AddStudentForm(AddUserForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial")
        initial.update({"role": "S"})
        super(AddStudentForm, self).__init__(args, kwargs)

    student_group = forms.ModelChoiceField(
        required=True, queryset=Group.objects.filter(is_active=True))


class AddPsychologistForm(AddUserForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial")
        initial.update({"role": "P"})
        super(AddPsychologistForm, self).__init__(args, kwargs)


class AddAdministratorForm(AddUserForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial")
        initial.update({"role": "A"})
        super(AddAdminForm, self).__init__(args, kwargs)


class AddInstitutionForm(forms.ModelForm):

    class Meta:
        model = Institution
        fields = [
            "nit",
            "name",
            "address",
            "city",
            "phone",
            "website",
            "is_active"
        ]

    nit = forms.CharField(
        label="Número de Nit",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Número de Nit"}))

    name = forms.CharField(
        label="Nombre instutución",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Nombre instutución"}))
    address = forms.CharField(
        label="Dirección de la institución",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Dirección de la institución"}))
    city = forms.CharField(
        label="Cuidad",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Cuidad"}))
    phone = forms.CharField(
        label="Número de teléfono",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Número de teléfono"}))
    website = forms.URLField(label="Sitio Web")

    is_active = forms.BooleanField(required=False)


class AddGroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = [
            "name",
            "grade",
            "schedule",
            "institution",
            "is_active"
        ]

    name = forms.CharField(
        label="Nombre del Group",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Nombre del Group"}))
    grade = forms.CharField(
        label="Grado del Group",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Grado del Group"}))
    schedule = forms.ChoiceField(
        label="Jornada del Group",
        widget=forms.Select, choices=SCHEDULE_OPTIONS)

    institution = forms.ModelChoiceField(
        queryset=Institution.objects.filter(is_active=True))

    is_active = forms.BooleanField(required=False)


class EditUserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "document_type",
            "document_number",
            "first_name",
            "last_name",
            "address",
            "phone",
            "email",
            "password",
        ]

    document_type = forms.ChoiceField(
        required=True, widget=forms.RadioSelect, choices=DOCUMENT_OPTIONS)
    document_number = forms.CharField(
        required=True, label="Número de documento",
        widget=forms.TextInput(
            attrs={"size": 25, "title": "Número de documento"}))
    first_name = forms.CharField(
        required=True, label="Primer Nombre",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Nombre"}))
    last_name = forms.CharField(
        required=True, label="Apellido",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Apellido"}))
    address = forms.CharField(
        required=True, label="Dirección de Residencia",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Dirección de Residencia"}))
    phone = forms.CharField(
        required=True, label="Número de teléfono",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Número de teléfono"}))

    email = forms.EmailField(
        required=True, label="Email", widget=forms.TextInput())
    password = forms.CharField(
        required=True, label="Contraseña", widget=forms.PasswordInput())
