# -*- coding:utf-8 -*-
from django import forms
from models import (Institution, Group, User)
from models import (DOCUMENT_OPTIONS, GENDER_OPTIONS,
                    ROLE_OPTIONS, SCHEDULE_OPTIONS)


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
            "group",
            "is_active"
        ]

    DATEPICKER = {
        "type": "text",
        "class": "form-control",
        "id": "datetimepicker4"
    }

    document_type = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect, choices=DOCUMENT_OPTIONS)
    document_number = forms.CharField(
        required=True, label="Número de documento",
        widget=forms.TextInput(
            attrs={"size": 25, "title": "Número de documento"}))
    gender = forms.ChoiceField(
        required=True,
        widget=forms.Select, choices=GENDER_OPTIONS)
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
        required=True, label="Email",
        widget=forms.TextInput())
    password = forms.CharField(
        required=True, label="Contraseña",
        widget=forms.PasswordInput(render_value=False))
    role = forms.ChoiceField(
        required=True,
        widget=forms.Select, choices=ROLE_OPTIONS)

    group = forms.ModelChoiceField(
        required=False, queryset=Group.objects.filter(is_active=True))

    is_active = forms.BooleanField(required=False)

    # def clean(self):
    # 	return self.cleaned_data


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
        required=True, label="Número de Nit",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Número de Nit"}))

    name = forms.CharField(
        required=True, label="Nombre instutución",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Nombre instutución"}))
    address = forms.CharField(
        required=True, label="Dirección de la institución",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Dirección de la institución"}))
    city = forms.CharField(
        required=True, label="Cuidad",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Cuidad"}))
    phone = forms.CharField(
        required=True, label="Número de teléfono",
        widget=forms.TextInput(
            attrs={"size": 20, "title": "Número de teléfono"}))
    website = forms.URLField(
        required=True, label="Sitio Web")

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
        required=True, label="Nombre del Group",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Nombre del Group"}))
    grade = forms.CharField(
        required=True, label="Grado del Group",
        widget=forms.TextInput(
            attrs={"size": 30, "title": "Grado del Group"}))
    schedule = forms.ChoiceField(
        required=True, label="Jornada del Group",
        widget=forms.Select, choices=SCHEDULE_OPTIONS)

    institution = forms.ModelChoiceField(
        required=True, queryset=Institution.objects.filter(is_active=True))

    is_active = forms.BooleanField(required=False)
