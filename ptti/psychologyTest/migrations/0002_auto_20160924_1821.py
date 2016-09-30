# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psychologyTest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Lgtbi')], max_length=2, verbose_name='G\xe9nero'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='rol',
            field=models.CharField(choices=[('ADMIN', 'Masculino'), ('PSI', 'Psic\xf3logo'), ('EST', 'Estudiante')], default='ADMIN', max_length=5, verbose_name='Rol'),
        ),
    ]
