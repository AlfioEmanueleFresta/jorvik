# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competenza',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Competenza CRI',
                'verbose_name_plural': 'Competenze CRI',
            },
        ),
        migrations.CreateModel(
            name='CompetenzaPersonale',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('creazione', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('ultima_modifica', models.DateTimeField(auto_now=True, db_index=True)),
                ('competenza', models.ForeignKey(to='curriculum.Competenza')),
                ('persona', models.ForeignKey(to='anagrafica.Persona', related_name='competenze_personali')),
            ],
            options={
                'verbose_name': 'Competenza personale',
                'verbose_name_plural': 'Competenze personali',
            },
        ),
        migrations.CreateModel(
            name='Titolo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Titoli',
            },
        ),
        migrations.CreateModel(
            name='TitoloPersonale',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('creazione', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('ultima_modifica', models.DateTimeField(auto_now=True, db_index=True)),
                ('confermata', models.BooleanField(verbose_name='Confermata', default=True, db_index=True)),
                ('ritirata', models.BooleanField(verbose_name='Ritirata', default=False, db_index=True)),
                ('persona', models.ForeignKey(to='anagrafica.Persona', related_name='titoli_personali')),
                ('titolo', models.ForeignKey(to='curriculum.Titolo')),
            ],
            options={
                'verbose_name': 'Titolo personale',
                'verbose_name_plural': 'Titoli personali',
            },
        ),
    ]
