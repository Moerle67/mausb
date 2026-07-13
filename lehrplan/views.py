from django.shortcuts import render, get_list_or_404, redirect

from .models import Fachrichtung, Thema, Lerneinheit, Ausbildungseinheit

from stammdaten.classForm import *
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
        antwort += "<div><details class='p-2 border'>"
        antwort += f"<summary><a class='text-bg-secondary' href='/admin/lehrplan/ausbildungseinheit/{ae.id}/change/' target='__empty'>{ae}</a> <a href='/inh/add/{ae.id}' title='Neues untergeordnetes Element'><i class='bi bi-plus-circle text-bg-secondary'></i></a></summary>"
        for child_ae in lst_ae:
            antwort += f"<a class='text-bg-secondary' href='/admin/lehrplan/ausbildungseinheit/{ae.id}/change/' target='__empty'>{get_details_ae(child_ae)}</a>"
        antwort += "</details><div>"
    else:
        antwort += f"<p ><a class='text-bg-secondary' href='/admin/lehrplan/ausbildungseinheit/{ae.id}/change/' target='__empty'>{ae}</a> <a href='/inh/add/{ae.id}'><i class='bi bi-plus-circle text-bg-secondary'></i></a></p>"

    return antwort

def add(request, id):
    if request.method == "POST":
        if id == 0:
            ds_ausbildungseinheit = None
        else:
            ds_ausbildungseinheit= get_list_or_404(Ausbildungseinheit, id = id)[0]
        ds_ae = Ausbildungseinheit()
        ds_ae.thema         = ds_ausbildungseinheit
        ds_ae.inhalt        = request.POST['Inhalt']
        ds_ae.beschreibung  = request.POST['Beschreibung']
        ds_ae.time          = request.POST['Zeit in AE']
#        ds_ae.ausbilder     = request.user

        ds_ae.save()

        return redirect("/inh/start2")
    else:
        # Neues Formular
        print(id)
        if id == 0:
            ds_ausbildungseinheit = ("Neues Thema",)
        else:
            ds_ausbildungseinheit= get_list_or_404(Ausbildungseinheit, id = id)

        print(ds_ausbildungseinheit)
        frm_parent = FormInput("ÜbergeordneteLE", str(ds_ausbildungseinheit[0]), readonly=True)
        frm_inhalt = FormInput("Inhalt")
        frm_beschreibung = FormTextArea("Beschreibung")
        frm_zeit = FormInput("Zeit in AE", type="number", value = "0")

        forms = (frm_parent, frm_inhalt, frm_beschreibung, frm_zeit, formLinie, FormBtnOk)

        content = {
            'ueber': "Neue Ausbildungseinheit",
            'forms' : forms,
        }
        return render(request, "stammdaten/form.html", content) 

