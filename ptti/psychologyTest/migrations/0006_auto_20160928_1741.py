# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 17:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('psychologyTest', '0005_auto_20160928_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='institucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit', models.CharField(max_length=15, verbose_name='Nit')),
                ('nombre', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=30)),
                ('ciudad', models.CharField(max_length=30)),
                ('telefono', models.CharField(max_length=20)),
                ('sitio_web', models.CharField(max_length=30)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='perfil_estudiante',
            name='grupo',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil_estudiante',
            name='institucion',
            field=models.CharField(max_length=20),
        ),
    ]
