from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import json

from .models import Daytime, Block
from stammdaten.models import Team, Gruppe, AbwesendMA, Ausbilder
from lehrplan.models import Lerneinheit

import datetime
# Create your views here.

def start(request, team=None, date=None):
    """Hauptanzeige

    Args:
        request: Daten vom Browser
        team (int optional): ID Team.Stammdaten
        date (String, optional): Datum: "dd.mm.yyyy"

    Returns:
        HttpResponse_
    """

    date_format_str = "%d.%m.%Y"
    if not team:                                            # Kein Team vorgegeben                                               
        team = Team.objects.filter(activ = True).first()    # Auswahl erstes Team in DB
        return redirect(reverse('ausbildungsplan:team', kwargs={'team':team.id}))
    else:
        team = get_object_or_404(Team, id=team)             # Lese Team von ID

    if not date:                                            # kein Datum angegeben --> heute()
        date = datetime.date.today()
        return redirect(reverse('ausbildungsplan:date', 
                                kwargs={
                                    'team': team.id,
                                    'date': date.strftime(date_format_str),
                                }))
    else:
        date = datetime.datetime.strptime(date, date_format_str).date()
    # Tagsezeiten
    vm_ds = Daytime.objects.get(short="vm")
    nm_ds = Daytime.objects.get(short="nm")
    daytimes = (vm_ds, nm_ds)

    # Listen bschäfftigter Mitarbeiter
    besch_ma = []
    # Montag bestimmen
    date_moday = date - datetime.timedelta(days=date.weekday())
    days = []                           # Wochentage als String
    days_date = []                      # Wochentage als Date Objekt
    abwesend_lst =[[], [], [], [], []]  # Abwesenheit nach Wochentagen
    for day in range(5):
        date = date_moday + datetime.timedelta(days=day)
        days.append(date.strftime(date_format_str))
        days_date.append(date)
        aubi_anwesend_lst = AbwesendMA.objects.filter(date=date)    # Abwesenheit nach Datum
        abwesend_lst[day] = list(aubi_anwesend_lst)
        aubi_anwesend_lst = list(AbwesendMA.objects.filter(day=day))
        for element in aubi_anwesend_lst:                           # Regelmäßige Abwesenheit
            abwesend_lst[day].append(element)
                          
    daten_plan = []
    gruppen = []
    # Gruppen der Teams aussuchen
    gruppen_lst = Gruppe.objects.filter(team=team, activ=True)
    ma_beschaeftigt = [[[], [], [], [], []], [[], [], [], [], []]]
    # daten_plan.append(days)
    for gruppe in gruppen_lst:
        eine_gruppe = []                # Liste für eine Gruppe
        eine_gruppe.append(gruppe)      
        # Einzelne Wochentage
        eine_gruppe_days = []

        # Block Tageszeiten
        daytime_cnt = 0
        for daytime in daytimes:
            plan = []
            besch_ma_day = []
            day_cnt = 0    
            for day in days_date:    
                block = Block.objects.filter(group = gruppe, date = day, daytime = daytime)
                if len(block) != 0:
                    teacher =  block[0].teacher
                    ma_le_lst = Lerneinheit.objects.filter(ausbilder=teacher)
                else:
                    ma_le_lst = None

                block = None if len(block) == 0 else block[0]
                plan.append((block, ma_le_lst))

                # Mitarbeiter in Liste "beschäftigt" eintragen
                if block:
                    ma_beschaeftigt[daytime_cnt][day_cnt].append(block.teacher)
                day_cnt += 1
            besch_ma.append(besch_ma_day)        # Mitarbeiter beschäftigt((vm: Tag1 - Tag5),(nm: Tag1 - Tag5))               
            eine_gruppe_days.append(plan)
            daytime_cnt += 1
        eine_gruppe.append(eine_gruppe_days)
        gruppen.append(eine_gruppe)
    daten_plan.append(gruppen)
    # Freie Mitarbeiter
    # Alle Mitarbeiter laden
    ma_lst = list(team.aubi.filter(activ=True))
    freie_ma_lst = [[[], [], [], [], []], [[], [], [], [], []]]
    # Mitarbeiter in Liste beschäftigt suchen
    # Vormittag, Nachmittag
    for daytime in range(2):
        for day in range(5):
            # Mitarbeiterliste kopieren
            freie_ma_lst[daytime][day] = ma_lst.copy()
            # Beschäftigte Mitarbeiter abziehen
            for element in ma_beschaeftigt[daytime][day]:
                if element in freie_ma_lst[daytime][day]:
                    freie_ma_lst[daytime][day].remove(element)
            # Abwesende Mitarbeiter abziehen
            for element in abwesend_lst[day]:  
                if element.aubi in freie_ma_lst[daytime][day]:               # MA noch frei?
                    if element.daytime == "gt":                         # Ganztags
                        freie_ma_lst[daytime][day].remove(element.aubi)
                    if daytime == 0 and element.daytime == "am":        # Vormittag
                        freie_ma_lst[daytime][day].remove(element.aubi)                    
                    if daytime == 1 and element.daytime == "pm":        # Nachmittag
                        freie_ma_lst[daytime][day].remove(element.aubi)
                    

    content = {
        'team': team,
        'days': days,
        'daytimes': daytimes,
        'gruppen_plan': gruppen,
        'freie_ma': freie_ma_lst,
        'abw_ma': abwesend_lst,
        'date_html': date.strftime("%Y-%m-%d"), 
    }
    return render(request, "ausbildungsplan/plan.html", content)

def ausw_pp(request):

    # Ausbilder aus DB lesen
    aubi_id = request.POST['ausbilder'].split('_')[1]
    aubi_ds = get_object_or_404(Ausbilder, id = aubi_id, activ = True)

    # Gruppe aus Datenbank lesen
    group_ds = get_object_or_404(Gruppe, id = request.POST['group'], activ = True)

    # Datum
    date = datetime.datetime.strptime(request.POST['monday'], "%d.%m.%Y").date()+datetime.timedelta(days=int(request.POST['days']))

    # Blockobjekt erstellen oder überschreiben
    block_ds, create = Block.objects.get_or_create(
        group = group_ds,
        date = date,
        daytime = Daytime.objects.get(short="vm") if request.POST['daytime'] == '0' else Daytime.objects.get(short="nm")
    )
    block_ds.teacher = aubi_ds
    block_ds.save()
    # Rückgabe
    answer = {
            'error': False,
        }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def rem_block(request):
    block_ds = get_object_or_404(Block, id = int(request.POST['block_id']))
    aubi = block_ds.teacher
    block_ds.delete()
    answer = {
            'aubi_id': aubi.id,
            'aubi_name': aubi.user.last_name,
            'aubi_fg': aubi.fg_color,
            'aubi_bg': aubi.bg_color,
            'error': False,
        }
    return HttpResponse(json.dumps(answer), content_type="application/json")  
  
def save_content(request):
    """Content Block speichern
    
    Daten Ajax
    id, content

    Args:
        request (_type_): _description_
    """
    ds_block = get_object_or_404(Block, id = int(request.POST["id"]))
    ds_block.content = request.POST["content"]
    ds_block.save()
    answer = {
            'error': False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def add_abwpp(request):
    """Abwesende Mitarbeiter Plug & Play
        Request Form
        id      - Mitarbeiter ID
        date    - Datum Montag
        day     - Wochentag 0-4
    Args:
        request (_type_): _description_
    """

    ma_id       = request.POST['id'].split('_')[1]
    date_monday = request.POST['date']
    day         = int(request.POST['day'])

    aubi_ds = Ausbilder.objects.get(id=ma_id)
    date = datetime.datetime.strptime(date_monday, "%d.%m.%Y") + datetime.timedelta(days= day)

    ds_besch = AbwesendMA(aubi=aubi_ds, date=date)
    ds_besch.save()

    answer = {
        'error': False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")


