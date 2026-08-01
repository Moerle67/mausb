from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse

# Datenbanken
from .models import Tn_fa
from anwesenheit.models import TNAnwesend
from stammdaten.models import Gruppe, Teilnehmer

import datetime, json
from django.contrib.auth.decorators import permission_required

# from stammdaten.models import Teilnehmer
# Create your views here

@permission_required('frageantwort.view_tnanwesend', raise_exception=True)
def start(request, gruppe):
    ##
    # Status Teinehmer
    # 0 - neu
    # 1 - positive Antwort
    # 2 - negative Anwort
    # Hole alle anwesenden Teilnehmer
    # erst Gruppe
    ds_gruppe = get_list_or_404(Gruppe, id=gruppe)

    lst_tn_anw = get_lstanw(gruppe)

    lst_tn_fa = []
    lst_tn_anw = get_lstanw(gruppe)
    lst_zufall = []

    for tn in lst_tn_anw:
        ds_teilnehmer = Tn_fa.objects.filter(teilnehmer=tn, datum__date = datetime.date.today()).order_by('-datum').first()

        if ds_teilnehmer:
            comment = ds_teilnehmer.comment
            if ds_teilnehmer.status == 1:
                status = 1
            elif ds_teilnehmer.status == 2:
                status = 2
            else:
                status = 0

        else:
            comment = ""
            status = 0

        # Liste für Zufallsauswahl
        if status == 0 or status == 1:
            lst_zufall.append(tn.id)
        lst_tn_fa.append((tn, status, comment))
    lst_ueb = ("Offen", "2.Chance", "Gut")
    content = {
        'gruppe'        : gruppe,
        'liste'         : lst_tn_fa, 
        'lst_ueb'       : lst_ueb,
        'lst_zufall'    : lst_zufall,
    }
    return render(request, "frageantwort/start.html", content) 

def get_lstanw(gruppe):
    # Liste anwesende TN gemerieren

    lst_tn = Teilnehmer.objects.filter(group = gruppe)
    lst_tn_anw = []
    for teilnehmer in lst_tn:
        ds_tn_anw = TNAnwesend.objects.filter(datum__date = datetime.date.today(), teilnehmer=teilnehmer).order_by('-datum').first()
        # letzter Eintrag war "anwesend"
        if ds_tn_anw and ds_tn_anw.anwesend:
            lst_tn_anw.append(teilnehmer)
    return lst_tn_anw

def savetn(request):
    ###
    # Ajax
    # Speichert Antwort 
    ds_fa = Tn_fa()
    ds_tn = get_list_or_404(Teilnehmer, id=int(request.POST['tn']))[0]
    ds_fa.teilnehmer = ds_tn
    ds_fa.status =  int(request.POST['code'])
    ds_fa.comment = request.POST['thema']

    ds_fa.save()

    answer = {
        'error': False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def newlst(request):
    # Liste zurück setzen
    gruppe              = request.POST['gruppe']
    # List anwesener TN holen
    lst_tn_anw  = get_lstanw(gruppe)
    for tn in lst_tn_anw:
        ds = Tn_fa()
        ds.teilnehmer   = tn
        ds.status       = 0
        ds.save()

    answer = {
        'error': False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def get_tn(request):
    tn = int(request.POST['id'])
    ds = get_object_or_404(Teilnehmer, id=tn)
    answer = {
        'name'      : ds.name,
        'error'     : False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")
