from django.shortcuts import get_object_or_404, render
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
    zykl        = False if request.POST['zykl'] == "false" else True
    aufgabe     = request.POST['aufgabe']
    bereich     = request.POST['bereich']
    info        = request.POST['info']
    verant      = request.POST['verant']
    termin      = request.POST['termin']
    prio        = request.POST['prio']
    
    ds_task = Aufgabe()

    ds_task.ueber = aufgabe
    ds_task.bereich = Bereich.objects.get(id=bereich)
    ds_task.inhalt = info
    ds_task.verantwortlich = User.objects.get(id=verant)
    ds_task.termin = None if termin == "" else termin
    ds_task.prio = prio
    ds_task.ersteller = request.user
    ds_task.zyklisch = zykl

    ds_task.save()
    element = f"""  <a class="btn btn-outline-dark m-2 shadow col" data-bs-toggle="collapse" href="#ce_{ds_task.id}" role="button" aria-expanded="false" aria-controls="collapseExample">
                        {ds_task.ueber}
                    </a>

                    <div class="collapse col-12" id="ce_{ds_task.id}">
                        <div class="card card-body">
                            {ds_task.inhalt}
                        </div>
                    </div>
    """
    ds_id = ds_task.id

    answer = {
        'id'        : ds_id, 
        'error'     : False,
        'element'   : element,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

def task_dnd(request):
    id      = int(request.POST['id'])
    target  = request.POST['target']
    ds_task = get_object_or_404(Aufgabe, id = id)

    match target:
        case "lst_todo":
            ds_task.aktiv   = True
            ds_task.aktuell = False
            print("todo")
        case "lst_progr":
            ds_task.aktiv   = True
            ds_task.aktuell = True
            print("progr")
        case "lst_done":
            ds_task.aktiv   = False
            ds_task.aktuell = False
            print("done")
    ds_task.save()

    answer = {
        'error'     : False,
    }
    return HttpResponse(json.dumps(answer), content_type="application/json")
