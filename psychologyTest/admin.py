# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Institution, Group, User

# Unregister the Django Group table
from django.contrib.auth.models import Group as Django_Group
admin.site.unregister(Django_Group)


class ProfileAdminUser(admin.ModelAdmin):
    list_display = ["document_type", "document_number", "gender", "first_name",
                    "last_name", "birthdate", "address", "phone", "email",
                    "role", "is_active", "join_date", "last_login"]

    class Meta:
        model = User


class ProfileAdminInstutucion(admin.ModelAdmin):
    list_display = ["nit", "name", "address", "city", "phone",
                    "website", "is_active", "creation_date", "modified_date"]

    class Meta:
        model = Institution


class ProfileAdminGroup(admin.ModelAdmin):
    list_display = ["name", "grade", "schedule", "institution",
                    "is_active", "creation_date", "modified_date"]

    class Meta:
        model = Group

admin.site.register(User, ProfileAdminUser)
admin.site.register(Institution, ProfileAdminInstutucion)
admin.site.register(Group, ProfileAdminGroup)
