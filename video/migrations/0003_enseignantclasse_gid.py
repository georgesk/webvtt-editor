# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_enseignantclasse'),
    ]

    operations = [
        migrations.AddField(
            model_name='enseignantclasse',
            name='gid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
