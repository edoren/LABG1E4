# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group as Django_Group

# Register your models here.
from .models import (AssignTestKolb, Group, Institution, StudentGroup,
                     TestKolb, TestKolbQuestion, User)

admin.site.unregister(Django_Group)


class ProfileUser(admin.ModelAdmin):
    list_display = ["id", "document_type", "document_number", "gender",
                    "first_name", "last_name", "birthdate", "address", "phone",
                    "email", "role", "is_active", "join_date", "last_login"]

    class Meta:
        model = User


class ProfileInstutucion(admin.ModelAdmin):
    list_display = ["id", "nit", "name", "address", "city", "phone",
                    "website", "is_active", "creation_date", "modified_date"]

    class Meta:
        model = Institution


class ProfileGroup(admin.ModelAdmin):
    list_display = ["id", "name", "grade", "schedule", "institution",
                    "is_active", "creation_date", "modified_date"]

    class Meta:
        model = Group


class ProfileStudentGroup(admin.ModelAdmin):
    list_display = ["id", "student", "group"]

    class Meta:
        model = StudentGroup


class ProfileTestKolb(admin.ModelAdmin):
    list_display = ["id", "name", "description", "psychologist"]

    class Meta:
        model = TestKolb


class ProfileTestKolbQuestion(admin.ModelAdmin):
    list_display = ["id", "test", "description",
                    "option1", "option2", "option3", "option4"]

    class Meta:
        model = TestKolbQuestion


class ProfileAssignTestKolb(admin.ModelAdmin):
    list_display = ["id", "student", "test"]

    class Meta:
        model = AssignTestKolb


admin.site.register(User, ProfileUser)
admin.site.register(Institution, ProfileInstutucion)
admin.site.register(Group, ProfileGroup)
admin.site.register(StudentGroup, ProfileStudentGroup)
admin.site.register(TestKolb, ProfileTestKolb)
admin.site.register(TestKolbQuestion, ProfileTestKolbQuestion)
admin.site.register(AssignTestKolb, ProfileAssignTestKolb)
