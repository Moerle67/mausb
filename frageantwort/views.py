from django.shortcuts import render, get_list_or_404

from .models import Tn_fa
from anwesenheit.models import TNAnwesend
from stammdaten.models import Gruppe, Teilnehmer

import datetime
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
    content = {
        'liste'          : lst_tn_fa, 
    }    
