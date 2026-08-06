from django.shortcuts import render, get_list_or_404, get_object_or_404

from stammdaten.models import Gruppe
# Create your views here.

def start(request):
    return

def add_klas(request, team):
    ds_team         = get_object_or_404(Gruppe, id = team)
    lst_gruppen     = Gruppe.objects.filter(team = ds_team, activ = True)


    content = {
        'gruppen'           : lst_gruppen,
    }