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

@permission_required('stammdaten.view_gruppe', raise_exception=True)
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


@permission_required('anwesenheit.add_tnanwesend', raise_exception=True)
def anw_detail(request, id, aim_date=None):
    # aim_date != today --> Auswertung, Änderungen werden blockiert
    if aim_date == None:
        datum = datetime.date.today()
        passiv = False
    else:
        passiv = True
        datum = datetime.datetime.strptime(aim_date, "%Y-%m-%d").date()
        if datum == datetime.date.today():    # --> doch aktueller Tag, Änderungen möglich
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
@permission_required('anwesenheit.add_tnanwesend', raise_exception=True)
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
@permission_required('stammdaten.add_tnanmerkung', raise_exception=True)
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

@permission_required('anwesenheit.view_sitzplan', raise_exception=True)
def anw_raum(request, group, date):
    group = get_object_or_404(Gruppe, id = group)
    raum = group.raum
    lst_tn = Teilnehmer.objects.filter(group=group, activ=True)
    lst_teilnehmer= []
    for tn in lst_tn:
        if len(Sitzplan.objects.filter(raum = raum, teilnehmer = tn)) == 0:
            lst_teilnehmer.append(tn)

    elements = []
    if raum:
        for reihe in range(raum.row):
            lst_reihe = []
            for spalte in range(raum.col):
                plan =  Sitzplan.objects.filter(row=reihe, col=spalte, raum=raum)
                if len(plan)>0: #Teilnehmer am Platz vorhanden
                    # Anwesenheit aktueller Tag prüfen
                    akt_datum = datetime.date.today()
                    anw_ds = TNAnwesend.objects.filter(teilnehmer = plan[0].teilnehmer, datum__date = akt_datum)
                    if len(anw_ds) == 0 :         # kein Datensatz --> keine aktuelle Buchung
                        bg_color_code = "bg-secondary bg-gradient"
                    else:                       # DS vorhanden, nach Datum sortiert, der letzte gilt
                        bg_color_code = "bg-success bg-gradient" if anw_ds[0].anwesend else "bg-danger bg-gradient"
                    lst_reihe.append((plan[0], bg_color_code))
                else:
                    lst_reihe.append(None)   
            elements.append(lst_reihe)  
    content = {
        'gruppe': group,
        'raum': raum,
        'elements': elements,
        'teilnehmer': lst_teilnehmer,
    }
    return render(request, "anwesenheit/anw_plan.html", content)

@permission_required('anwesenheit.change_sitzplan', raise_exception=True)
# Sitzplatz speichern D&D
def saveplan(request):
    raum = request.POST['raum']
    teilnehmer = request.POST['teilnehmer']
    spalte = request.POST['spalte']
    zeile = request.POST['zeile']
    ds_raum = get_object_or_404(Raum, id=raum)
    ds_teilnehmer = get_object_or_404(Teilnehmer, id=teilnehmer)
  
    ds_sitz, create = Sitzplan.objects.get_or_create(raum=ds_raum, row = zeile, col = spalte)

    ds_tn_alt = ds_sitz.teilnehmer
    ds_sitz.teilnehmer = ds_teilnehmer
    ds_sitz.save()

    # Anwesenheitsfarbe ermitteln
    ds_tn_anw = TNAnwesend.objects.filter(teilnehmer=ds_teilnehmer, datum__date = datetime.date.today())
    if len(ds_tn_anw) == 0:
        bg_color = "bg-secondary"
    else:
        bg_color = "bg-success" if ds_tn_anw[0].anwesend else "bg-danger"

    answer = {
        'error': False,
        'teilnehmer': ds_teilnehmer.__str__(),
        'teilnehmer_id': ds_teilnehmer.id,
        'teilnehmer_old': ds_tn_alt.__str__(),
        'tno_id': ds_tn_alt.id if ds_tn_alt else None,
        'tn_picture': ds_sitz.teilnehmer.picture.url,
        'bg_color': bg_color,
        'plan_id': ds_sitz.id, 
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

@permission_required('anwesenheit.delete_sitzplan', raise_exception=True)
def delplan(request):
    ds = get_object_or_404(Sitzplan, id=int(request.POST['id']))
    ds_teilnehmer = ds.teilnehmer
    zeile = ds.row
    spalte = ds.col
    ds.delete()
    answer = {
        'zeile': zeile,
        'spalte': spalte,
        'error': False,
        'teilnehmer_id': ds_teilnehmer.id,
        'teilnehmer': ds_teilnehmer.__str__(),
        'tn_picture': ds_teilnehmer.picture.url,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

# Anwesenheit aus Sitzplan speichern
@permission_required('anwesenheit.add_tnanwesend', raise_exception=True)
def savedateplan(request):
    ds_tn = get_object_or_404(Teilnehmer, id=request.POST['teilnehmer'])

    # Aktuelle Anwesenheit?
    ds_tn_anw = TNAnwesend.objects.filter(teilnehmer=ds_tn, datum__date = datetime.date.today())
    if len(ds_tn_anw)==0 :              # Noch keine Eintragung erstmal abwesend
        anwesenheit = False
    else:                               # ansonsten Gegenteil der letzten Eintragung
        anwesenheit = not ds_tn_anw[0].anwesend
    # Ausbilder ermitteln
    ds_ausbilder = get_object_or_404(Ausbilder, user=request.user)
    # DS erzeugen
    ds = TNAnwesend(teilnehmer = ds_tn, ausbilder = ds_ausbilder, anwesend = anwesenheit)
    # DS speichern
    ds.save()
      
    # Hintergrundfarbe festlegen
    bg_color_code = "bg-success" if anwesenheit else "bg-danger"

    #Sitzplan lesen
    ds_sitzplan = Sitzplan.objects.get(teilnehmer=ds_tn)

    answer = {
        'bg_color': bg_color_code,
        'zeile': ds_sitzplan.row,
        'spalte': ds_sitzplan.col,
        'error': False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")
