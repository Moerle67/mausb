from django.shortcuts import render

from stammdaten.classForm import FormInput, formLinie, FormBtnOk
# Create your views here.
def start(request):
    if request.GET is not None:
        if "next" in request.GET:
            cont = request.GET["next"]
        else:
            cont = "start:start"
    content = {
        'cont': cont,
    }   
    return render(request, "start/start.html", content)
