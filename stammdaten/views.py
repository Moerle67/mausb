from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from task.models import Aufgabe
from .models import *

import json
# Create your views here.

def start(request):
    return HttpResponse("Startseite")

def user_login(request):
    name = request.POST['name']
    password = request.POST['password']
    cont = request.POST['cont']
    user = authenticate(request, username=name, password=password)
    if user is not None:
        login(request, user)
    if ":" in cont:                     # url auflösen
        cont = reverse(cont)
    return redirect(cont)
    # Redirect to a success page.

def user_logout(request):

    logout(request)
    # Auf Startseite umleiten
    return redirect("/")

# Userlogin über Ajax
def ajax_login(request):
    name = request.POST['name']
    password = request.POST['password']
    user = authenticate(request, username=name, password=password)
    if user is not None:
        login(request, user)
        print(f"{user} angemeldet")
        answer = {
            'error'     : False,
        }
    else:
        answer = {
            'error'     : True,
        }   
    return HttpResponse(json.dumps(answer), content_type="application/json")

# Abfrage laufender Tasks
def task(request):
    if request.user.id != None:
        user = request.user
        task = Aufgabe.objects.filter(aktiv = True, verantwortlich=user, aktuell = False).count()
        answer = {
            'error': False,
            'task': task,
        }
    else:
        answer = {
            'error': True,
        }
    return HttpResponse(json.dumps(answer), content_type="application/json")

# Leilnehmer mit Liste abgleichen
def abgleich(request):
    lst_tn_neu = []
    lst_grp_neu = []

    lst_tn_old = []

    str_stg = "-S-"
    lst_rios = TN_rios.objects.all()
    ds_renningen = Team.objects.get(name="Renningen")
    for tnr in lst_rios:
        short_massnahme = tnr.massnahme.split(str_stg)[0]
        # Beruf lesen
        beruf = Beruf.objects.filter(short=short_massnahme)
        if beruf:
            # IT-ler
            gruppe = "IT-S-"+tnr.massnahme.split(str_stg)[1]
        else:
            # Keine IT
            gruppe = tnr.massnahme
        ds_gruppe = Gruppe.objects.filter(name=gruppe)
        if not ds_gruppe:
            # Gruppe muss neu erstellt werden
            ds_gruppe = Gruppe()
            ds_gruppe.name=gruppe
            ds_gruppe.short=gruppe
            ds_gruppe.team = ds_renningen
            ds_gruppe.save()
            lst_grp_neu.append(ds_gruppe)
        else:
            ds_gruppe = ds_gruppe[0]
        name = tnr.nachname+", "+tnr.vorname
        # Nach TN Nummer suchen
        ds_tn = Teilnehmer.objects.filter(tn_number=tnr.id)
        if not ds_tn:
            # Alternativ nach Namen suchen
            ds_tn = Teilnehmer.objects.filter(name=name)
            if ds_tn:
               ds_tn[0].tn_number=tnr.id
               ds_tn[0].save()
            # Auch nicht, neu erfasssen 
            ds_tn = Teilnehmer()
            ds_tn.name = name
            ds_tn.group = ds_gruppe
            ds_tn.tn_number = tnr.id
            ds_tn.save()
            lst_tn_neu.append(ds_tn)

    # Nach fehlenden Teilnehmern suchen
    lst_tn = Teilnehmer.objects.all()
    for tn in lst_tn:
        ds_tn_rios = TN_rios.objects.filter(id = tn.tn_number)
        if len(ds_tn_rios) == 0:
            lst_tn_old.append(tn)
    # print("Neue Teilnehmer: ",lst_tn_neu)
    # print("Neue Gruppe: ", lst_grp_neu)
    # print("Fehlende Teilnehmer: ", lst_tn_old)
    content = {
        'tn_new': lst_tn_neu,
        'grp_new': lst_grp_neu,
        'tn_old': lst_tn_old,
    }
    return render(request, "stammdaten/abgleich.html", content)
