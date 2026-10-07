from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.http import HttpResponse

from .models import *

from stammdaten.models import Gruppe

import json

# Create your views here.

def start(request, schrank = -1):
    lst_schrank = Schrank.objects.all()
    if schrank == -1:
        # ersten Schrank auswählen
        schrank = lst_schrank[0].id
    ds_schrank = get_object_or_404(Schrank, id = schrank)
    lst_gruppen  = Gruppe.objects.all()

    lst_tn = Teilnehmer.objects.filter(group=lst_gruppen[0].id)
    ##########################
    # Fachbelegung
    # 0 - unbelegt
    # 1 - belegt
    # 2 - unbekannt
    #
    startnumber = ds_schrank.start
    zeilen = []
    for zeile in range(ds_schrank.hoehe):
        spalten = []
        for spalte in range(ds_schrank.breite):
            number = startnumber + zeile * ds_schrank.breite + spalte
            lst_fach = Fach.objects.filter(number=number)
            if len(lst_fach) == 0:
                # Fach unbelegt
                spalten.append((number, 0,))
            else:
                # Fach belegt
                spalten.append((number, 1, lst_fach[0].user))
        zeilen.append(spalten)
    content = {
        'schraenke'     : lst_schrank,
        'schrank_akt'   : ds_schrank,
        'zeilen'        : zeilen,
        'gruppen'       : lst_gruppen,
        'teilnehmer'    : lst_tn,
    }
    return render(request, "faecher/start.html", content)

def get_user(gruppe):
    #####################
    #
    # Liste aller Mitglieder einer Gruppe ohne Fach
    #

    liste = []
    lst_user = Teilnehmer.objects.filter(activ = True, group = gruppe)
    for user in lst_user:
        ds_fach = Fach.objects.filter(user=user.id)
        if len(ds_fach)==0:
            liste.append(user)


def get_fach(request):
    fach = request.POST['fach']

    ds_fach = get_object_or_404(Fach, number=fach)
    str_tn = get_slct_tn(ds_fach.user.group.id, ds_fach.user.id)
    str_gr = get_slct_gruppe(ds_fach.user.group.id)
    datertn = ds_fach.belegtbis 

    answer = {
        'error': False,
        'lst_tn' : str_tn,
        'lst_gr' : str_gr,
        'datern' : datertn.strftime("%Y-%m-%dT00:00"),
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def get_slct_tn(gruppe, teilnehmer):
    lst_tn = get_list_or_404(Teilnehmer, group=gruppe)
    str_tn = ""
    #str_tn  = f"<select class = 'form-select' id = 'sct_tn' onchange = 'onchange_sct_tn(this)'>"
    for tn in lst_tn:
        str_slc = "selected " if tn.id == teilnehmer else ""
        str_tn += f"<option value='{tn.id}' {str_slc}>{tn}</option>"
    # str_tn += "</select>"
    return str_tn

def get_slct_gruppe(gruppeid):
    lst_gr = Gruppe.objects.all()
    str_gr = ""
    for gruppe in lst_gr:
        str_slc = "selected " if gruppe.id == gruppeid else ""
        str_gr += f"<option value='{gruppe.id}' {str_slc}>{gruppe}</option>"
    # str_tn += "</select>"
    return str_gr

