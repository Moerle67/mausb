from django.shortcuts import render
from django.contrib.auth.models import User
import json
from django.http import HttpResponse


from .models import Aufgabe, Bereich

# Create your views here.

def start(request):
    user = request.user
    todo_lst = Aufgabe.objects.filter(verantwortlich = user, aktiv = True, aktuell = False)
    progress_lst = Aufgabe.objects.filter(verantwortlich = user, aktiv = True, aktuell = True)
    zykl_lst = Aufgabe.objects.filter(verantwortlich = user, aktiv = False, zyklisch = True )
    done_lst = Aufgabe.objects.filter(verantwortlich = user, aktiv = False, zyklisch = False)

    content = {
        'todo'      : todo_lst,
        'progress'  : progress_lst,
        'zykl'      : zykl_lst,
        'done'      : done_lst,
    }

    return render(request, 'task/task_start.html', content)

def get_task_form(request):
    # select für Befreich generieren
    lst_bereich = Bereich.objects.all()
    str_bereich = ""
    for zeile in lst_bereich:
        str_bereich += f'<option value = "{zeile.id}">{zeile.name}</option>'
    
    # Liste möglicher Verantwortlicher generieren
    lst_verant = User.objects.filter(is_active = True)
    str_verant = ""
    for zeile in lst_verant:
        str_verant += f'<option value = "{zeile.id}">{zeile.last_name}, {zeile.first_name}</option>'

    answer = {
        'bereich'   : str_bereich,
        'verant'    : str_verant,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def save_task_form(request):
    zykl = False if request.POST['zykl'] == "false" else True
    aufgabe = request.POST['aufgabe']
    print(zykl, aufgabe)
    answer = {
        'error'   : False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")
