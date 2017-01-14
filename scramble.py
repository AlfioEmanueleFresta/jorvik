# -*- coding: utf-8 -*-

import os, sys
import random

from datetime import timedelta
from django.db import transaction

from base.comuni import COMUNI

os.environ['DJANGO_SETTINGS_MODULE'] = 'jorvik.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from anagrafica.permessi.applicazioni import PRESIDENTE, UFFICIO_SOCI, DELEGATO_OBIETTIVO_1, DELEGATO_OBIETTIVO_2

import phonenumbers
from django.db import IntegrityError
from django.db.models import Count

from anagrafica.costanti import NAZIONALE, PROVINCIALE, TERRITORIALE, REGIONALE, LOCALE
from autenticazione.models import Utenza
from base.utils import poco_fa
from base.utils_tests import crea_persona, email_fittizzia, codice_fiscale_persona
from veicoli.models import Autoparco
from base.geo import Locazione


from anagrafica.models import Sede, Persona, Appartenenza, Delega
import argparse


__author__ = 'alfioemanuele'

parser = argparse.ArgumentParser(description='Mischia i dati anagrafici.')

parser.add_argument('--membri-sede', dest='membri_sedi', action='append',
                   help='dato pk di una sede, mischia i dati degli appartenenti passati e attuali')
parser.add_argument('--dati-di-esempio', dest='esempio', action='store_const',
                    default=False, const=True,
                    help='installa dei dati di esempio')
parser.add_argument('--aggiorna-province', dest='province', action='store_const',
                    default=False, const=True,
                    help='aggiorna le province')

args = parser.parse_args()



def ottieni_random():  # Ottiene una persona a caso.
    numero = Persona.objects.aggregate(count=Count('id'))['count']
    while True:
        try:
            num = random.randint(0, numero - 1)
            p = Persona.objects.all()[num]
            return p
        except Persona.DoesNotExist:
            pass

def oscura(stringa, percentuale):
    out = ""
    for r in range(len(stringa)):
        out += stringa[r] if stringa[r] in ['@', '.'] or random.randint(0,100) > percentuale else chr(random.randint(64,90))
    return out

if args.membri_sedi:
    print("Avvio miscelatore anagrafico.")

for sede in (args.membri_sedi if args.membri_sedi else []):
    sede = Sede.objects.get(pk=sede)
    membri = Persona.objects.filter(appartenenze__sede__in=sede.get_descendants())
    totale = membri.count()
    print("Sede %s: Trovati %d membri." % (sede, totale,))
    contatore = 0

    for membro in membri:
        contatore += 1
        membro.nome = ottieni_random().nome
        membro.cognome = ottieni_random().cognome
        membro.save()

        tentativi_cf = 0
        while True:
            try:
                tentativi_cf += 1
                nuovo_codice_fiscale = oscura(ottieni_random().codice_fiscale, 50)
                membro.codice_fiscale = nuovo_codice_fiscale
                membro.save()
                break

            except IntegrityError:  # Riprova fino a che CF univoco
                pass

        tentativi_email_contatto = 0
        while True:
            try:
                tentativi_email_contatto += 1
                membro.email_contatto = oscura(ottieni_random().email_contatto, 35)
                membro.save()
                break

            except IntegrityError:  # Riprova fino a che CF univoco
                pass

        tentativi_utenza = 0
        try:
            if membro.utenza and not membro.utenza.is_staff:
                while True:
                    try:
                        tentativi_utenza += 1
                        utenza = membro.utenza
                        nuova_email = oscura(utenza.email, 75).lower()
                        utenza.email = nuova_email
                        utenza.save()
                        break

                    except IntegrityError:  # Riprova fino a che CF univoco
                        pass
        except:
            pass

        print("Miscelato %d di %d (%f percento): T.CF %d, T.EC %d, T.EU %d" % (
            contatore, totale, (contatore/totale*100), tentativi_cf, tentativi_email_contatto, tentativi_utenza)
        )

if args.esempio:
    print("Installo dei dati di esempio")

    with transaction.atomic():
        Utenza.objects.all().delete()
        Persona.objects.all().delete()
        Appartenenza.objects.all().delete()
        Delega.objects.all().delete()
        Sede.objects.all().delete()

    print("Creo le Sedi fittizie...")
    italia = Sede.objects.create(nome="Comitato Nazionale", estensione=NAZIONALE)
    regionale = Sede.objects.create(nome="Comitato Regione 1", estensione=REGIONALE, genitore=italia)
    altra_regione = Sede.objects.create(nome="Comitato Regione 2", estensione=REGIONALE, genitore=italia)
    c = Sede.objects.create(nome="Comitato di Gaia", genitore=regionale, estensione=LOCALE)
    s1 = Sede.objects.create(nome="York", genitore=c, estensione=TERRITORIALE)
    s2 = Sede.objects.create(nome="Bergamo", genitore=c, estensione=TERRITORIALE)
    s3 = Sede.objects.create(nome="Catania", genitore=c, estensione=TERRITORIALE)
    c2 = Sede.objects.create(nome="Altro Comitato di Gaia", genitore=altra_regione, estensione=LOCALE)
    c3 = Sede.objects.create(nome="Comitato Fittizio", genitore=regionale, estensione=LOCALE)
    a1 = Autoparco(nome="Autorimessa Principato", sede=s3)
    a1.save()

    presidente = None

    print("Genero dei membri della Sede a caso con deleghe e cariche ...")
    print(" - Creo persone...")
    sedi = [c, s1, s2, s3, c2, c3, regionale, altra_regione]
    for sede in sedi:  # Per ogni Sede
        locazione = Locazione.oggetto(indirizzo=random.sample(COMUNI.keys(), 1)[0])
        sede.locazione = locazione
        sede.save()
        for membro in [Appartenenza.VOLONTARIO, Appartenenza.SOSTENITORE]:
            for i in range(0, 25):  # Creo 20 volontari
                p = crea_persona()
                p.comune_nascita = random.sample(COMUNI.keys(), 1)[0]
                p.codice_fiscale = codice_fiscale_persona(p)
                p.save()
                data = poco_fa() - timedelta(days=random.randint(10, 5000))
                a = Appartenenza.objects.create(persona=p, sede=sede, inizio=data, membro=membro)
                if i % 5 == 0 and membro == Appartenenza.VOLONTARIO:
                    data_precedente = data - timedelta(days=random.randint(10, 500))
                    altra = random.sample(sedi, 1)[0]
                    a = Appartenenza.objects.create(
                        persona=p, sede=altra, inizio=data_precedente, fine=data, membro=membro,
                        terminazione=Appartenenza.DIMISSIONE
                    )
        for i in range(0, 5):  # Creo 5 aspiranti
            p = crea_persona()
            p.comune_nascita = random.sample(COMUNI.keys(), 1)[0]
            p.codice_fiscale = codice_fiscale_persona(p)
            p.save()
            p.ottieni_o_genera_aspirante()

        if sede.estensione in (LOCALE, REGIONALE):
            print(" - Assegno deleghe...")
            persone = [a.persona for a in Appartenenza.objects.filter(sede=sede, membro=Appartenenza.VOLONTARIO).order_by('?')[:4]]
            for indice, persona in enumerate(persone):
                if indice == 0:
                    d = Delega.objects.create(persona=persona, tipo=PRESIDENTE, oggetto=sede, inizio=poco_fa())
                    if sede == c:
                        # Grazie per tutto il pesce
                        persona.nome = "Douglas"
                        persona.cognome = "Adams"
                        persona.codice_fiscale = codice_fiscale_persona(persona)
                        persona.save()
                        presidente = persona
                        # Assegno una utenza
                        if not Utenza.objects.filter(email="supporto@gaia.cri.it").exists():
                            utenza = Utenza(persona=persona, email="supporto@gaia.cri.it",
                                            password='pbkdf2_sha256$20000$ldk8aPLgcMXK$Cwni1ubmmKpzxO8xM75ZuwNR+k6ZHA5JTVxJFbgIzgo=')
                            utenza.save()
                elif indice == 1:
                    d = Delega.objects.create(persona=persona, tipo=UFFICIO_SOCI, oggetto=sede, inizio=poco_fa())
                elif indice == 2:
                    d = Delega.objects.create(persona=persona, tipo=DELEGATO_OBIETTIVO_1, oggetto=sede, inizio=poco_fa())
                elif indice == 3:
                    d = Delega.objects.create(persona=persona, tipo=DELEGATO_OBIETTIVO_2, oggetto=sede, inizio=poco_fa())

    print(" - Creo utenze di accesso...")
    for persona in Persona.objects.all().exclude(pk=presidente.pk):
        utenza = Utenza.objects.create_user(
            persona=persona, email=email_fittizzia(),
            password=email_fittizzia()
        )

    print("= Fatto.")

if args.province:
    print("Aggiorno le province")

    province = Locazione.objects.filter(stato="IT").exclude(provincia='').values_list('provincia', flat=True).distinct()

    for provincia in province:
        prima = Locazione.objects.filter(provincia=provincia).first()
        prima.cerca_e_aggiorna()
        pv = prima.provincia_breve

        altre = Locazione.objects.filter(provincia=provincia)
        num = altre.update(provincia_breve=pv)

        print("-- %s\t%d\t%s" % (pv, num, provincia))



print("Finita esecuzione.")
