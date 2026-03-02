from django.shortcuts import render

from .models import Fachrichtung, Thema, Lerneinheit
# Create your views here.

def start(request):
    lst_fachrichtungen_db = Fachrichtung.objects.all()
    lst_fachrichtungen = []
    for fachrichtung in lst_fachrichtungen_db:
        lst_themen_db = Thema.objects.filter(fachrichtung=fachrichtung)
        lst_thema = []
        for thema in lst_themen_db:
            lst_lerneinheit_db = Lerneinheit.objects.filter(thema=thema)
            lst_thema.append((thema, lst_lerneinheit_db))
        lst_fachrichtungen.append((fachrichtung, lst_thema))   
    
    content = {
        'lst_fachrichtungen': lst_fachrichtungen
    }
    return render(request, "lehrplan/start.html", content)
