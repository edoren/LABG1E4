# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 17:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psychologyTest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentgroup',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='psychologyTest.Group'),
        ),
        migrations.AlterUniqueTogether(
            name='studentgroup',
            unique_together=set([('student', 'group')]),
        ),
    ]
