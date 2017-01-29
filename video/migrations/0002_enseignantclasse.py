# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 14:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnseignantClasse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classe', models.CharField(max_length=50)),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.Enseignant')),
            ],
        ),
    ]