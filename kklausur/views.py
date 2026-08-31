from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse

from stammdaten.models import Gruppe

from . import renderers

# Create your views here.

from .models import *
def start(request):
    return

def add_klas(request, team):
    ds_team         = get_object_or_404(Gruppe, id = team)
    lst_gruppen     = Gruppe.objects.filter(team = ds_team, activ = True)


    content = {
        'gruppen'           : lst_gruppen,
    }

@permission_required('klausur.view_teilnehmer')
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
