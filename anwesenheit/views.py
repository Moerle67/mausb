import json
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import User

from stammdaten.models import Team, Gruppe, Teilnehmer, Ausbilder
from .models import TNAnwesend

import stammdaten.classForm as cform 

from datetime import date, timezone
from django.utils.timezone import activate

# Create your views here.

def start(request):
    # Erstaufruf zur Auswahl des Teams
    teams = Team.objects.filter(activ = True)
    # Nur ein Team?
    if len(teams)==1 :
        return redirect(f"/anw/{teams[0].id}")
    
    teams = cform.FormAuswahl("Teams", Team, leerzeile=True, aktiv=True, onclick='anw_group(this.value)')
    
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

def anw_detail(request, id, datum=-1):
    gruppe = get_object_or_404(Gruppe, id=id)
    team = gruppe.team
    groups = Gruppe.objects.filter(activ=True, team=team)

    teams = cform.FormAuswahl("Teams", Team, leerzeile=True, aktiv=True, value=team.id,  onclick='anw_group(this.value)')
    select_groups = cform.FormAuswahl("Gruppe", daten=groups, leerzeile=True, value=id, onclick='anw_detail(this.value)')

    tn_group = Teilnehmer.objects.filter(activ=True, group=gruppe)
    elements = []
    for tn in tn_group:
        ds = TNAnwesend.objects.filter(teilnehmer=tn, datum__date = date.today())
        if len(ds)>0:
            anwesend = ds[0].anwesend
            code = 1 if anwesend else 2
            str_anw = ""
            for termin in ds:
                color = "text-success" if termin.anwesend else "text-danger"
                time = termin.datum.strftime("%H:%M")
                str_anw += f'<i class="bi bi-circle-fill me-2 ' + color +'"></i>' + time +'; '
        else:
            code = 0
            str_anw = ""
        elements.append((tn, code, ds, str_anw))

    content = {
        'cont': 'anw:start',
        'teams': teams,
        'groups': select_groups,
        'teilnehmer': elements,
        
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
        }
        return HttpResponse(json.dumps(answer), content_type="application/json")
    else:
        answer = {
            'error': True,
        }
        return HttpResponse(json.dumps(answer), content_type="application/json")