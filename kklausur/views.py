from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse

from stammdaten.models import Gruppe

from . import renderers

import datetime, json

# Create your views here.

from .models import *

@permission_required('stammdaten.show_gruppe')
def start(request, team = 1):
    lst_groups = Gruppe.objects.filter(team=team)

    content = {
        'gruppen'     :lst_groups,
    } 
    return render(request, "kklausur/start.html", content)

@permission_required('kklausur.show_klausur')
def ausw_klausur(request, gruppe):
    ds_gruppe       = get_object_or_404(Gruppe, id=gruppe)
    lst_gruppen     = Gruppe.objects.filter(team = ds_gruppe.team)
    lst_klausur     = Klausur.objects.filter(gruppe = gruppe)

    # Letzte Klausur auswählen, wenn vorhanden
    if len(lst_klausur) > 0:
        return redirect("klausur:detail_klausur", klausur = lst_klausur[0].id)
    
    content = {
        'gruppen'           : lst_gruppen,
        'gruppe_aktiv'      : ds_gruppe.id,
        'klausuren'         : lst_klausur,
        'klausur_aktiv'     : "-",
    }
    return render(request, "kklausur/aklausur.html", content)

@permission_required('kklausur.add_klausur')
def new_klausur(request, gruppe):
    morgen = datetime.datetime.now() + datetime.timedelta(days=1)
    ds_gruppe = get_object_or_404(Gruppe, id = gruppe)
    ds_klausur = Klausur(gruppe = ds_gruppe, datum = morgen, title = "Neue Klausur")
    ds_klausur.save()
    return redirect("klausur:detail_klausur", klausur = ds_klausur.id)

@permission_required('kklausur.add_klausur')
def detail_klausur(request, klausur):
    ds_klausur = get_object_or_404(Klausur, id = klausur)
    ds_gruppe       = get_object_or_404(Gruppe, id=ds_klausur.gruppe.id)
    lst_gruppen     = Gruppe.objects.filter(team = ds_klausur.gruppe.team.id)
    lst_klausur     = Klausur.objects.filter(gruppe = ds_klausur.gruppe.id)
    lst_themen      = Ausbildungseinheit.objects.all()
    # date_time = now.strftime("%Y-%m-%dT%H:%M")  
    # str_date     = "2027-06-12T19:30"
    str_date        =  ds_klausur.datum.strftime("%Y-%m-%dT%H:%M") 

    content = {
        'gruppen'           : lst_gruppen,
        'gruppe_aktiv'      : ds_gruppe.id,
        'klausuren'         : lst_klausur,
        'klausur_aktiv'     : ds_klausur.id,

        'klausur_detail'    : ds_klausur,
        'themen'            : lst_themen,
        'str_date'          : str_date,
    }
    return render(request, "kklausur/detail_klausur.html", content)

@permission_required('kklausur.show_klausur')
def chg_klausur_title(request):
    ds_klausur = get_object_or_404(Klausur, id = request.POST['klausur'])
    ds_klausur.title = request.POST['title']
    ds_klausur.save()

    answer = {
            'error': False,
        }
    return HttpResponse(json.dumps(answer), content_type="application/json")

@permission_required('kklausur.change_klausur')
def chg_klausur_thema(request):
    ds_klausur  = get_object_or_404(Klausur, id = request.POST['klausur'])
    ds_thema    =  get_object_or_404(Ausbildungseinheit, id = request.POST['thema'])
    ds_klausur.thema = ds_thema
    ds_klausur.save()

    answer = {
            'error': False,
        }
    return HttpResponse(json.dumps(answer), content_type="application/json")


@permission_required('kklausur.change_klausur')
def chg_klausur_termin(request):

    ds_klausur          = get_object_or_404(Klausur, id = request.POST['klausur'])
    ds_klausur.datum    = datetime.datetime.strptime(request.POST['datum'], "%Y-%m-%dT%H:%M")
    ds_klausur.save()

    answer = {
            'error': False,
        }
    return HttpResponse(json.dumps(answer), content_type="application/json")


@permission_required('kklausur.show_klausur')
def gen_pdf(request, klausur, typ = 1):
    # typ 1 - Klausur 
    #     2 - Muster
    #     3 - Design Fragen
    #     4 - Design Muster
    klausur = Klausur.objects.get(pk=klausur)
    fragen = []
    if typ == 1 or typ == 2:
        lst_fragen = KlausurFrage.objects.filter(klausur = klausur)
        for kfrage in lst_fragen:
            fragen.append((kfrage, kfrage.startnp))

    thema = klausur.title
    punkte = klausur.get_gesamtpunkte
    termin = klausur.datum.date()
    context = {
        'pdf_title' : klausur,
        'klausur'   : klausur,
        'fragen'    : fragen,
        'termin'    : termin,
        'punkte'    : punkte,
        'thema'     : thema,
        'gruppe'    : klausur.gruppe,
    }
    if typ == 1 or typ == 3: # Klausur
        response = renderers.render_to_pdf("pdfs/klausur_gen.html", context)
    elif typ == 2 or typ == 4: # Muster
        response = renderers.render_to_pdf("pdfs/muster_gen.html", context)        
    
    if response.status_code == 404:
        raise Http404("Invoice not found")

    filename = f"Klausur_{thema}.pdf"
    """
    Tell browser to view inline (default)
    """
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        """
        Tells browser to initiate download
        """
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response
