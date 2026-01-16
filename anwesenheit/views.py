from django.shortcuts import redirect, render

# Create your views here.

def start(request):
    content = {
        'cont': 'anw:start',
    }

    return render(request,"anwesenheit/start.html", content)

