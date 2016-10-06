# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psychologyTest', '0002_auto_20160924_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rol',
            field=models.CharField(choices=[('ADMIN', 'Administrador'), ('PSI', 'Psic\xf3logo'), ('EST', 'Estudiante')], default='ADMIN', max_length=5, verbose_name='Rol'),
        ),
    ]