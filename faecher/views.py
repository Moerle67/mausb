from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render

from .models import *

from stammdaten.models import Gruppe
# Create your views here.

def start(request, schrank = -1):
    lst_schrank = Schrank.objects.all()
    if schrank == -1:
        # ersten Schrank auswählen
        schrank = lst_schrank[0].id
    ds_schrank = get_object_or_404(Schrank, id = schrank)
    lst_gruppen  = Gruppe.objects.all()

    belegung = []
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
    }
    return render(request, "faecher/start.html", content)

