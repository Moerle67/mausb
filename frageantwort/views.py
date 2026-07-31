from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse

# Datenbanken
from .models import Tn_fa
from anwesenheit.models import TNAnwesend
from stammdaten.models import Gruppe, Teilnehmer

import datetime, json

# from stammdaten.models import Teilnehmer
# Create your views here.

def start(request, gruppe):
    ##
    # Status Teinehmer
    # 0 - neu
    # 1 - positive Antwort
    # 2 - negative Anwort
    # Hole alle anwesenden Teilnehmer
    # erst Gruppe
    ds_gruppe = get_list_or_404(Gruppe, id=gruppe)
    lst_tn = Teilnehmer.objects.filter(group = gruppe)
    lst_tn_anw = []
    for teilnehmer in lst_tn:
        ds_tn_anw = TNAnwesend.objects.filter(datum__date = datetime.date.today(), teilnehmer=teilnehmer).order_by('-datum').first()
        # letzter Eintrag war "anwesend"
        if ds_tn_anw and ds_tn_anw.anwesend:
            lst_tn_anw.append(teilnehmer)
    lst_tn_fa = []
    for tn in lst_tn_anw:
        ds_teilnehmer = Tn_fa.objects.filter(teilnehmer=tn, datum__date = datetime.date.today()).order_by('-datum').first()
        if ds_teilnehmer:
            if ds_teilnehmer.status == 1:
                status = 1
            else:
                status = 2
        else:
            status = 0
        lst_tn_fa.append((tn, status))
    print(lst_tn_fa)
    lst_ueb = ("Offen", "2.Chance", "Gut")
    content = {
        'liste'          : lst_tn_fa, 
        'lst_ueb'          : lst_ueb,
    }
    return render(request, "frageantwort/start.html", content) 

def savetn(request):
    ds_fa = Tn_fa()
    ds_tn = get_list_or_404(Teilnehmer, id=int(request.POST['tn']))
    ds_fa.teilnehmer = ds_tn
    ds_fa.status =  request.POST['code']
    ds_fa.save()

    answer = {
        'error': False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")
