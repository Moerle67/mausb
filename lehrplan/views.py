from django.shortcuts import render

from .models import Fachrichtung, Thema, Lerneinheit, Ausbildungseinheit
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

def start2(request):
    lst_top_themen = Ausbildungseinheit.objects.filter(thema = None)
    liste = []
    lst_ae = ""
    for top_thema in lst_top_themen:
        liste.append((top_thema, get_lst_ae(top_thema)))
    # print(liste)
    for element in lst_top_themen:
        test = get_details_ae(element)
        print(test)
        lst_ae += test
    content = {
        'lst_fachrichtungen'  : None,
        'lst_ae'              : lst_ae             
    }   
    return render(request, "lehrplan/start2.html", content)

def get_lst_ae(ae):
    # alle Child-Elemente finden
    lst_ae = Ausbildungseinheit.objects.filter(thema=ae)
    if len(lst_ae) == 0 :
        return (None)
    else:
        lst_ae_child = []
        for element in lst_ae:
            lst_ae_child.append((element,get_lst_ae(element)))
        return lst_ae_child
    
def get_details_ae(ae):
    antwort = ""
    # Children laden
    lst_ae = Ausbildungseinheit.objects.filter(thema=ae)
    
    # gibt es Children?
    if len(lst_ae) > 0:
        antwort += "<div><details class='p-2 border shadow'>"
        antwort += f"<summary>{ae}</summary>"
        for child_ae in lst_ae:
            antwort += get_details_ae(child_ae)
        antwort += "</details><div>"
    else:
        antwort += f"<p>{ae}</p>"

    return antwort


