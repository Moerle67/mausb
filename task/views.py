from django.shortcuts import render

from .models import Aufgabe

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

    return render(request, 'task/start.html', content)
