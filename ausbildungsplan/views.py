from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Daytime, Block
from stammdaten.models import Team, Gruppe

import datetime
# Create your views here.

def start(request, team=None, date=None):
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

    # Montag bestimmen
    date_moday = date - datetime.timedelta(days=date.weekday())
    days = []           # Wochentage als String
    days_date = []      # Wochentage als Date Objekt
    for i in range(5):
        day = date_moday + datetime.timedelta(days=i)
        days.append(day.strftime(date_format_str))
        days_date.append(day)

    daten_plan = []
    gruppen = []
    # Gruppen der Teams aussuchen
    gruppen_lst = Gruppe.objects.filter(team=team, activ=True)
    # daten_plan.append(days)
    for gruppe in gruppen_lst:
        eine_gruppe = []                # Liste für eine Gruppe
        eine_gruppe.append(gruppe)      
        # Einzelne Wochentage
        eine_gruppe_days = []
        # Block Vormittag
        plan_vm = []     
        for day in days_date:    
            block_vm = Block.objects.filter(group = gruppe, date = day, daytime = vm_ds)
            block_vm = None if len(block_vm) == 0 else block_vm[0]
            plan_vm.append(block_vm)
        eine_gruppe_days.append(plan_vm)
        # Block Nachmittag
        plan_nm = []
        for day in days_date:    
            block_nm = Block.objects.filter(group = gruppe, date = day, daytime = nm_ds)
            block_nm = None if len(block_nm) == 0 else block_nm[0]
            plan_nm.append(block_nm)
        eine_gruppe_days.append(plan_nm)

        eine_gruppe.append(eine_gruppe_days)
        gruppen.append(eine_gruppe)    
    daten_plan.append(gruppen)
    content = {
        'team': team,
        'days': days,
        'gruppen_plan': gruppen,
    }
    return render(request, "ausbildungsplan/plan.html", content)