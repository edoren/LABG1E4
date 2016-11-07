# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from psychologyTest.auth import UserManager


DOCUMENT_OPTIONS = (("TI", "Tarjeta de Identidad"),
                    ("CC", "Cedula de Ciudadania"),
                    ("CE", "Cedula de Extranjería"))
GENDER_OPTIONS = (("M", "Masculino"), ("F", "Femenino"), ("O", "Other"))
ROLE_OPTIONS = (("R", "Root"), ("A", "Administrador"),
                ("P", "Psicólogo"), ("S", "Estudiante"))
SCHEDULE_OPTIONS = (("Morning", "Mañana"), ("Afternoon", "Tarde"),
                    ("Evening", "Noche"), ("Saturday", "Sabatina"))


class User(AbstractBaseUser):
    document_type = models.CharField(
        max_length=5, choices=DOCUMENT_OPTIONS, default="CC")
    document_number = models.CharField(max_length=30)

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    birthdate = models.DateField(null=True, blank=False)
    gender = models.CharField(max_length=2, choices=GENDER_OPTIONS)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)

    role = models.CharField(max_length=1, choices=ROLE_OPTIONS,
                            null=False, blank=False)

    is_active = models.BooleanField(default=False, blank=False)
    join_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELD = [USERNAME_FIELD, "password"]

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def is_staff(self):
        return self.role == "R"

    def has_perm(self, perm, obj=None):
        return self.role == "R"

    def has_module_perms(self, package_name):
        return self.role == "R"

    def __str__(self):
        return u"{} {} [{}]".format(self.first_name, self.last_name,
                                    self.email)

    __unicode__ = __str__


class Institution(models.Model):
    nit = models.CharField(max_length=25)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    phone = models.CharField(max_length=25)
    website = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"{} - {}".format(self.nit, self.name)

    __unicode__ = __str__


class Group(models.Model):
    name = models.CharField(max_length=30)
    grade = models.CharField(max_length=15)
    schedule = models.CharField(max_length=30, choices=SCHEDULE_OPTIONS)

    institution = models.ForeignKey(Institution, null=False, blank=False)

    is_active = models.BooleanField(default=True, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    psychologist = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return u"{} {} {}".format(self.name, self.grade, self.schedule)

    __unicode__ = __str__


class StudentGroup(models.Model):
    student = models.ForeignKey(User, null=False, blank=False)
    group = models.ForeignKey(Group, null=False, blank=False)

    class Meta:
        unique_together = ("student", "group")


class TestKolb(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    psychologist = models.ForeignKey(User, null=False, blank=False)

    def __str__(self):
        return u"{}".format(self.name)

    __unicode__ = __str__


class TestKolbQuestion(models.Model):
    test = models.ForeignKey(TestKolb, null=False, blank=False)

    description = models.CharField(max_length=1000)
    option1 = models.CharField(max_length=150)
    option2 = models.CharField(max_length=150)
    option3 = models.CharField(max_length=150)
    option4 = models.CharField(max_length=150)


class AssignTestKolb(models.Model):
    student = models.ForeignKey(User, null=False, blank=False)
    test = models.ForeignKey(TestKolb, null=False, blank=False)
    is_finished = models.BooleanField(default=False, blank=False)

    class Meta:
        unique_together = ("student", "test")


class TestKolbAnswer(models.Model):
    question = models.ForeignKey(TestKolbQuestion, null=False, blank=False)
    assignation = models.ForeignKey(AssignTestKolb, null=False, blank=False)

    CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4))

    option1 = models.IntegerField(choices=CHOICES, null=True)
    option2 = models.IntegerField(choices=CHOICES, null=True)
    option3 = models.IntegerField(choices=CHOICES, null=True)
    option4 = models.IntegerField(choices=CHOICES, null=True)

    class Meta:
        unique_together = ("question", "assignation")
