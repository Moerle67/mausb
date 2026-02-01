import datetime
import json
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import User

from stammdaten.models import Team, Gruppe, Teilnehmer, Ausbilder, TNAnmerkung, Raum
from .models import TNAnwesend, Sitzplan

import stammdaten.classForm as cform

from django.contrib.auth.decorators import permission_required

# from datetime import date, datetime
from django.utils.timezone import activate

# Create your views here.

def start(request):
    # Erstaufruf zur Auswahl des Teams
    teams = Team.objects.filter(activ = True)
    # Nur ein Team?
    if len(teams)==1 :
        return redirect(f"/anw/{teams[0].id}")
    
    teams = cform.FormAuswahl("Teams", Team, leerzeile=True, aktiv=True, onclick='anw_group(this.value)')
    
   #
    content = {
        'cont': 'anw:start',            # Zurück bei Anmeldung
        'teams': teams,                 # Alle aktiven Teams
    }
    return render(request,"anwesenheit/anw_team.html", content)

@permission_required('stammdaten.gruppe_show')
def anw_group(request, id):
    # Auswahl der Gruppe
    team = get_object_or_404(Team, id=id)
    teams = cform.FormAuswahl("Teams", Team, leerzeile=True, aktiv=True, value=team.id,  onclick='anw_group(this.value)')
    groups = Gruppe.objects.filter(activ=True, team=team)
    select_groups = cform.FormAuswahl("Gruppe", daten=groups, leerzeile=True, onclick='anw_detail(this.value)')
    content = {
        'cont': 'anw:anw_g/1',
        'team': team,
        'teams': teams,
        'groups': select_groups,
    }
    return render(request,"anwesenheit/anw_group.html", content)

@permission_required('anwesenheit.tnanwesend_add')
def anw_detail(request, id, aim_date=-1):
    # aim_date != today --> Auswertung, Änderungen werden blockiert
    if aim_date == -1:
        datum = datetime.date.today()
        passiv = False
    else:
        passiv = True
        datum = datetime.datetime.strptime(aim_date, "%Y-%m-%d").date()
        # print(datum, datetime.date.today())
        if datum == datetime.date.today():    # --> doch aktueller Tag, Änderungen möglich
            print("gleich")
            passiv = False

    gruppe = get_object_or_404(Gruppe, id=id)
    team = gruppe.team
    groups = Gruppe.objects.filter(activ=True, team=team)

    teams = cform.FormAuswahl("Teams", Team, leerzeile=True, aktiv=True, value=team.id,  onclick='anw_group(this.value)')
    select_groups = cform.FormAuswahl("Gruppe", daten=groups, leerzeile=True, value=id, onclick='anw_detail(this.value)')

    tn_group = Teilnehmer.objects.filter(activ=True, group=gruppe)
    tn_count = len(tn_group)
    tn_count_anw = 0
    elements = []
    for tn in tn_group:
        ds = TNAnwesend.objects.filter(teilnehmer=tn, datum__date = datum)
        ds_notes = TNAnmerkung.objects.filter(teilnehmer=tn, date__date = datum)

        if len(ds)>0:
            anwesend = ds[0].anwesend
            code = 1 if anwesend else 2
            tn_count_anw += 1 if anwesend else 0                    # Anzahl der Anwesenden hochzählen
            str_anw = ""
            for termin in ds:
                color = "text-success" if termin.anwesend else "text-danger"
                icon = "hand-thumbs-up-fill" if termin.anwesend else "ban-fill"
                time = termin.datum.strftime("%H:%M")
                str_anw += f'<span title="'+termin.ausbilder.short+'"><i class="bi bi-'+ icon +' me-2 ' + color +'"></i>' + time +';</span> '
        else:
            code = 0
            str_anw = ""
        if len(ds_notes) > 0:       # Notizen vorhanden
            str_anw += '<span title="'
            for ds_note in ds_notes:
                str_anw += f"{ds_note.ausbilder.short} {ds_note.date.strftime("%H:%M")} - {ds_note.comment}\n"
            str_anw += '"><i class="bi bi-envelope me-2"></i>;</span>'


        elements.append((tn, code, ds, str_anw))

    content = {
        'cont': 'anw:start',
        'teams': teams,
        'groups': select_groups,
        'teilnehmer': elements,
        'aim_date': datum.strftime("%Y-%m-%d"),
        'gruppe': gruppe,
        'passiv': passiv,
        'count_tn': tn_count,
        'count_tn_anw': tn_count_anw
        
    }
    return render(request,"anwesenheit/anw_detail.html", content)

# Daten aus Formular speichern
def savedate(request):
    if request.method == 'POST':
        teilnehmer = request.POST['teilnehmer']
        anwesend = request.POST['anwesend']
        anwesend = True if anwesend=="true" else False
        ds_ausbilder = get_object_or_404(Ausbilder, user=request.user)
        ds_teilnehmer = get_object_or_404(Teilnehmer, id=teilnehmer)
        ds_termin = TNAnwesend(teilnehmer=ds_teilnehmer, anwesend=anwesend, ausbilder = ds_ausbilder)
        ds_termin.save()
        answer = {
            'error': False,
            'time': ds_termin.datum.strftime("%H:%M"),
            'ausbilder': ds_termin.ausbilder.short,
        }
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        answer = {
            'error': True,
        }
        return HttpResponse(json.dumps(answer), content_type="application/json")

# Notiz über Teilnehmer    
def anw_note(request):
    ds_tn = get_object_or_404(Teilnehmer, id=request.POST['tn'])
    ds_ausbilder = get_object_or_404(Ausbilder, user=request.user)
    ds  = TNAnmerkung(teilnehmer=ds_tn, ausbilder= ds_ausbilder, comment = request.POST['note'])
    ds.save()
    answer = {
        'error': False,
        'ausbilder': ds.ausbilder.short,
        'note': ds.comment,
        'time': ds.date.strftime('%d.%m.%Y %H:%M'),
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def anw_raum(request, group, date):
    group = get_object_or_404(Gruppe, id = group)
    lst_tn = Teilnehmer.objects.filter(group=group, activ=True)
    raum = group.raum
    elements = []
    if raum:
        for reihe in range(raum.row):
            lst_reihe = []
            for spalte in range(raum.col):
                plan =  Sitzplan.objects.filter(row=reihe, col=spalte, raum=raum)
                if len(plan)>0:
                    lst_reihe.append(plan[0].teilnehmer)
                else:
                    lst_reihe.append(".")   
            elements.append(lst_reihe)  
    content = {
        'raum': raum,
        'elements': elements,
        'teilnehmer': lst_tn,
    }
    return render(request, "anwesenheit/anw_plan.html", content)

def saveplan(request):

    raum = request.POST['raum']
    teilnehmer = request.POST['teilnehmer']
    spalte = request.POST['spalte']
    zeile = request.POST['zeile']
    ds_raum = get_object_or_404(Raum, id=raum)
    ds_teilnehmer = get_object_or_404(Teilnehmer, id=teilnehmer)
  
    ds_sitz, create = Sitzplan.objects.get_or_create(raum=ds_raum, row = zeile, col = spalte)
    ds_sitz.teilnehmer = ds_teilnehmer
    ds_sitz.save()

    answer = {
        'error': False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")
