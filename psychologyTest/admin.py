# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Institution, Group, User


class ProfileAdminUser(admin.ModelAdmin):
    list_display = ["document_type", "document_number", "gender", "first_name",
                    "last_name", "birthdate", "address", "phone", "email",
                    "password", "role", "is_active", "join_date", "last_login"]

    class Meta:
        model = User

admin.site.register(User, ProfileAdminUser)


class ProfileAdminInstutucion(admin.ModelAdmin):
    list_display = ["nit", "name", "address", "city", "phone",
                    "website", "is_active", "creation_date", "modified_date"]

    class Meta:
        model = Institution


admin.site.register(Institution, ProfileAdminInstutucion)


class ProfileAdminGroup(admin.ModelAdmin):
    list_display = ["name", "grade", "schedule", "institution",
                    "is_active", "creation_date", "modified_date"]

    class Meta:
        model = Group

admin.site.register(Group, ProfileAdminGroup)
