from django.shortcuts import render
from django.http import HttpResponse

import json

# Create your views here.

def bin(request, wert = 0):
    number, str_bin     = get_number(wert)

    content = {
        'str_bin'   : str_bin,
        'number'    : number,
        'wert'      : wert,
    }
    return render(request, "learn/bin.html", content) 

def set_bit(request):
    digit               = int(request.POST['number'])
    wert                = int(request.POST['wert'])
    liste, str_bin      = get_number(wert)
    if liste[digit][0] == 0:
        # Bit wird auf Eins gesetzt
        wert += 2**(7-digit)
    else:
        # Bit wird auf Null gesetzt
        wert -= 2**(7-digit)

    liste, str_bin      = get_number(wert)
    answer = {
        'str_bin'   : str_bin,
        'wert'      : wert,
        'potenz'    : 2**(7-digit),
        'error'     : False,

    }
    return HttpResponse(json.dumps(answer), content_type="application/json")

## IPV4 Klasse (irgendwann)

def get_number(wert):
    wert = int(wert)
    number = []
    str_bin = ""
    wertig = 128
    for i in range(8): 
        digit = 1 if wert >= wertig else 0
        if i == 4:
            str_bin += " "
        str_bin += str(digit)
        number.append((digit, wertig))
        wert -= digit * wertig
        wertig //= 2
    return number, str_bin



