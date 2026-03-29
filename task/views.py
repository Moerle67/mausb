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
    lst_bereich = Bereich.objects.all()
    str_bereich = '<select class="form-select" id="task-bereich">'
    for zeile in lst_bereich:
        str_bereich += f'<option value = "{zeile.id}">{zeile.name}</option>'
    str_bereich += '</select>'
    lst_verant = User.objects.filter(is_active = True)
    answer = {
        'bereich': str_bereich,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")
