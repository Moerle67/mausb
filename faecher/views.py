from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from .models import *

from stammdaten.models import Gruppe, Ausbilder

import json, datetime

# Create your views here.


@permission_required("faecher.view_fach")
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
                spalten.append((number, 1, lst_fach[0].user, lst_fach[0].belegtbis))
        zeilen.append(spalten)
    content = {
        'schraenke'     : lst_schrank,
        'schrank_akt'   : ds_schrank,
        'zeilen'        : zeilen,
        'gruppen'       : lst_gruppen,
        'teilnehmer'    : lst_tn,
    }
    return render(request, "faecher/start.html", content)

def save_fach(request):
    schrank = int(request.POST['schrank'])
    number = int(request.POST['number'])
    tn = int(request.POST['tn'])
    date = datetime.datetime.strptime(request.POST['date'], "%Y-%m-%d")

    ds_schrank = get_object_or_404(Schrank, id = schrank)
    if number < ds_schrank.start or number > ds_schrank.start+ds_schrank.breite*ds_schrank.hoehe-1:
        print(f"Falsche Fachnummer {number}")
        answer = {
            'msg': "Fachnummer gehört nicht zum Schrank",

            'error': True,
        }
        return HttpResponse(json.dumps(answer), content_type="application/json")
    
    ausbilder = get_object_or_404(Ausbilder, user=request.user.id)

    # Evtuell vorhandenes Fach löschen
    lst_fach = Fach.objects.filter(number = number)
    for fach in lst_fach:
        fach.delete()

    tn = get_object_or_404(Teilnehmer, id = tn)
    schrank = get_object_or_404(Schrank, id = schrank)

    ds_fach = Fach(
        user = tn, 
        number = number, 
        schrank = schrank,
        belegtbis = date,
        eingetragenvon = ausbilder
    )    
    ds_fach.save()
    answer = {
        'fach': ds_fach.user.__str__()+' - ' + ds_fach.belegtbis.strftime("%d. %B %Y"),

        'error': False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def del_fach(request):
    fach = request.POST['fach']
    ds_fach = get_object_or_404(Fach, number=fach)
    ds_fach.delete()
    
    answer = {
        'error': False,
    }

    return HttpResponse(json.dumps(answer), content_type="application/json")

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
        'error'     : False,
        'lst_tn'    : str_tn,
        'lst_gr'    : str_gr,
        'datern'    : datertn.strftime("%Y-%m-%d"),
        'str_fach'  : ds_fach.__str__()
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def get_group(request):
    group = request.POST['group']
    get_object_or_404(Gruppe, id = group)
    str_tn = get_slct_tn(group)

    answer = {
        'error': False,
        'slc_tn': str_tn,
        
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def get_slct_tn(gruppe, teilnehmer = None):
    lst_tn = get_list_or_404(Teilnehmer, group=gruppe)
    str_tn = "<option value='-'>-</option>"
    for tn in lst_tn:
        str_slc = "selected " if teilnehmer and tn.id == teilnehmer else ""
        str_tn += f"<option value='{tn.id}' {str_slc}>{tn}</option>"
    return str_tn

def get_slct_gruppe(gruppeid):
    lst_gr = Gruppe.objects.all()
    str_gr = ""
    for gruppe in lst_gr:
        str_slc = "selected " if gruppe.id == gruppeid else ""
        str_gr += f"<option value='{gruppe.id}' {str_slc}>{gruppe}</option>"
    return str_gr
