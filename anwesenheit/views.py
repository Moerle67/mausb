import datetime
import json
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import User

from stammdaten.models import Team, Gruppe, Teilnehmer, Ausbilder, TNAnmerkung
from .models import TNAnwesend

import stammdaten.classForm as cform

from datetime import date, datetime
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
        'cont': 'anw:start',
        'teams': teams,
    }
    return render(request,"anwesenheit/anw_team.html", content)

def anw_group(request, id):
    team = get_object_or_404(Team, id=id)
    teams = cform.FormAuswahl("Teams", Team, leerzeile=True, aktiv=True, value=team.id,  onclick='anw_group(this.value)')
    groups = Gruppe.objects.filter(activ=True, team=team)
    select_groups = cform.FormAuswahl("Gruppe", daten=groups, leerzeile=True, onclick='anw_detail(this.value)')
    content = {
        'cont': 'anw:anw_g',
        'team': team,
        'teams': teams,
        'groups': select_groups,
    }
    return render(request,"anwesenheit/anw_group.html", content)

def anw_detail(request, id, aim_date=-1):
    # aim_date != today --> Auswertung, Änderungen werden blockiert
    if aim_date == -1:
        datum = date.today()
        passiv = False
    else:
        passiv = True
        datum = date.strptime(aim_date, "%Y-%m-%d")
        print(datum, date.today())
        if datum == date.today():    # --> doch aktueller Tag, Änderungen möglich
            passiv = False

    gruppe = get_object_or_404(Gruppe, id=id)
    team = gruppe.team
    groups = Gruppe.objects.filter(activ=True, team=team)

    teams = cform.FormAuswahl("Teams", Team, leerzeile=True, aktiv=True, value=team.id,  onclick='anw_group(this.value)')
    select_groups = cform.FormAuswahl("Gruppe", daten=groups, leerzeile=True, value=id, onclick='anw_detail(this.value)')

    tn_group = Teilnehmer.objects.filter(activ=True, group=gruppe)
    elements = []
    for tn in tn_group:
        ds = TNAnwesend.objects.filter(teilnehmer=tn, datum__date = datum)
        ds_notes = TNAnmerkung.objects.filter(teilnehmer=tn, date__date = datum)
        if len(ds)>0:
            anwesend = ds[0].anwesend
            code = 1 if anwesend else 2
            str_anw = ""
            for termin in ds:
                color = "text-success" if termin.anwesend else "text-danger"
                icon = "hand-thumbs-up-fill" if termin.anwesend else "ban-fill"
                time = termin.datum.strftime("%H:%M")
                str_anw += f'<span title="'+termin.ausbilder.short+'"><i class="bi bi-'+ icon +' me-2 ' + color +'"></i>' + time +';</span> '
                if len(ds_notes) > 0:       # Notizen vorhanden
                    pass
        else:
            code = 0
            str_anw = ""
        elements.append((tn, code, ds, str_anw))

    content = {
        'cont': 'anw:start',
        'teams': teams,
        'groups': select_groups,
        'teilnehmer': elements,
        'aim_date': datum.strftime("%Y-%m-%d"),
        'gruppe': gruppe,
        'passiv': passiv,
        
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
