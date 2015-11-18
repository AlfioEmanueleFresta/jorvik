# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('creazione', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('ultima_modifica', models.DateTimeField(auto_now=True, db_index=True)),
                ('nome', models.CharField(default='Generale', max_length=256, db_index=True)),
                ('obiettivo', models.SmallIntegerField(default=1, db_index=True)),
            ],
            options={
                'verbose_name_plural': 'Aree',
            },
        ),
        migrations.CreateModel(
            name='Attivita',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('creazione', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('ultima_modifica', models.DateTimeField(auto_now=True, db_index=True)),
                ('nome', models.CharField(default='Nuova attività', max_length=255, db_index=True)),
                ('stato', models.CharField(default='B', max_length=1, choices=[('B', 'Bozza'), ('V', 'Visibile')], db_index=True)),
                ('apertura', models.CharField(default='A', max_length=1, choices=[('C', 'Chiusa'), ('A', 'Aperta')], db_index=True)),
                ('descrizione', models.TextField(blank=True)),
                ('area', models.ForeignKey(to='attivita.Area', related_name='attivita')),
                ('estensione', models.ForeignKey(default=None, to='anagrafica.Sede', null=True, related_name='attivita_estensione')),
            ],
            options={
                'verbose_name': 'Attività',
                'verbose_name_plural': 'Attività',
            },
            bases=(social.models.ConGiudizio, models.Model),
        ),
        migrations.CreateModel(
            name='Partecipazione',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('creazione', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('ultima_modifica', models.DateTimeField(auto_now=True, db_index=True)),
                ('confermata', models.BooleanField(verbose_name='Confermata', default=True, db_index=True)),
                ('ritirata', models.BooleanField(verbose_name='Ritirata', default=False, db_index=True)),
                ('stato', models.CharField(default='K', max_length=1, choices=[('K', 'Part. Richiesta'), ('X', 'Part. Ritirata'), ('N', 'Non presentato/a')], db_index=True)),
                ('persona', models.ForeignKey(to='anagrafica.Persona', related_name='partecipazioni')),
            ],
            options={
                'verbose_name': 'Richiesta di partecipazione',
                'verbose_name_plural': 'Richieste di partecipazione',
            },
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('creazione', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('ultima_modifica', models.DateTimeField(auto_now=True, db_index=True)),
                ('nome', models.CharField(default='Nuovo turno', max_length=128, db_index=True)),
                ('prenotazione', models.DateTimeField(verbose_name='Prenotazione entro', db_index=True)),
                ('inizio', models.DateTimeField(verbose_name='Inizio', db_index=True)),
                ('fine', models.DateTimeField(verbose_name='Fine', blank=True, default=None, null=True, db_index=True)),
                ('minimo', models.SmallIntegerField(default=1, db_index=True)),
                ('massimo', models.SmallIntegerField(default=None, null=True, db_index=True)),
                ('attivita', models.ForeignKey(to='attivita.Attivita', related_name='turni')),
            ],
            options={
                'verbose_name_plural': 'Turni',
            },
            bases=(models.Model, social.models.ConGiudizio),
        ),
        migrations.AddField(
            model_name='partecipazione',
            name='turno',
            field=models.ForeignKey(to='attivita.Turno', related_name='partecipazioni'),
        ),
    ]
