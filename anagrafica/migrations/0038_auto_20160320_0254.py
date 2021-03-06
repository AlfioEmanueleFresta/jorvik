# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-20 02:54
from __future__ import unicode_literals

import anagrafica.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0037_auto_20160311_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='email_contatto',
            field=models.EmailField(blank=True, max_length=255, validators=[anagrafica.validators.valida_email_personale], verbose_name='Email di contatto'),
        ),
    ]
