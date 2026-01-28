from django.shortcuts import render

from stammdaten.classForm import FormInput, formLinie, FormBtnOk
# Create your views here.
def start(request):
    return render(request, "start/start.html")

def login(request):
    name = FormInput("Anmeldename")
    """ Name

    Returns:
        _type_: _description_
    """    
    
    password = FormInput("Passwort")
    forms = (name, password, formLinie, FormBtnOk)
    content = {
        'forms': forms,
    }
    return render(request, "start/login.html", content)
