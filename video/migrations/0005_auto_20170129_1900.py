# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_atelier_travail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='travail',
            options={'verbose_name_plural': 'Travaux'},
        ),
        migrations.AlterField(
            model_name='travail',
            name='tt',
            field=models.TextField(default=''),
        ),
    ]
