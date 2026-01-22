class FormInput:
    label = ""
    type = ""
    required = True
    readonly = False
    disabled = False
    def __init__(self, label, value="", type="text", required = "True", disabled=False, readonly=False, submit=False):
        self.label = label
        self.value = value
        self.type = type
        self.required = required
        self.disabled = disabled
        self.readonly = readonly
        self.submit = submit

    def __str__(self):
        antwort = '<label for="'+self.label+'">'+self.label+'</label>\n'
        antwort += '<input '
        if self.submit:
            antwort+= ' onchange="this.form.submit()" '
        antwort += 'type="'+self.type+'" class="form-control" id="'+self.label+'" value="'+self.value
        antwort += '" name="'+self.label+'"'
        if self.required: 
            antwort += " required"
        if self.readonly:
            antwort += " readonly"
        if self.disabled:
            antwort += " disabled"
        antwort += '>\n'
        return antwort

class FormTextArea:
    label=""
    def __init__(self, label, value="", rows=4):
        self.label = label
        self.value = value
        self.rows = str(rows)

    def __str__(self):
        antwort =  f'<label for="{self.label}">{self.label}</label>\n'   
        antwort += f'<textarea class="form-control" id="{self.label}" name="{self.label}" rows="{self.rows}">'
        antwort += self.value
        antwort += "</textarea>"

        return antwort
class FormSlider:
    label = ""
    min = 0
    max = 10
    required = True
    readonly = False
    marks = True

    def __init__(self, label, value="0", required = "True", min=0, max=10, marks = True):
        self.label = label
        self.value = value
        self.min = min
        self.max = max
        self.required = required
        self.marks = marks
    def __str__(self):
        antwort = '<label for="'+self.label+'">'+self.label+'</label>\n'
        antwort += '<input type="range" class="form-control-range" id="'+self.label+'" value="'+str(self.value)
        antwort += '" name="'+self.label+'"'
        antwort += ' min="'+str(self.min)+'"'
        antwort += ' max="'+str(self.max)+'"'
        if self.marks:
            antwort += ' list="range'+self.label+'"'
        if self.required: 
            antwort += " required"
        if self.readonly:
            antwort += " readonly"
        antwort += '>\n'
        if self.marks:
            antwort += '<datalist id="range'+self.label+'">'
            for i in range(self.min, self.max+1):
                antwort += '<option value="'+str(i)+'" label="'+str(i)+'"></option>'
            antwort += '</datalist>'
        return antwort


class FormAuswahl:
    liste = ""
    value = ""
    name = ""
    def __init__(self, name, liste = False, daten=False, filter=False, value=0, aktiv=True, submit=False, label=True, leerzeile=False, onclick=False):
            self.liste = liste
            self.submit = submit
            self.label = label
            self.leerzeile = leerzeile
            self.onclick = onclick
            self.filter = filter
            self.daten = daten

            try:
                self.value = int(value)
            except:
                self.value = -1
            self.name = name
            self.aktiv = aktiv
            
    def __str__(self):
        if self.daten:
            daten = self.daten
        elif self.aktiv:
            daten = self.liste.objects.filter(activ=True )
        else:
            daten = self.liste.objects.filter()
        antwort=""    
        if self.label:
            antwort = '\n<label for="'+self.name+'">'+self.name+': </label>\n'
        antwort += '<select id="'+self.name+'" '
        if self.onclick:
            antwort+= f' onchange="{self.onclick}" '
        elif self.submit:
            antwort+= ' onchange="this.form.submit()" '
        antwort += 'name="'+self.name+'" class="form-control">\n'
        if self.leerzeile :
            antwort +="<option value='---'> --- </option>\n" 
        for zeile in daten:
            antwort += '<option value="'+str(zeile.id)+'"'
            if zeile.id == self.value:
                antwort += "selected "
            antwort +='>'+str(zeile)+'</option>\n'
        antwort += '</select>\n'


        return antwort

class FormBtn:
    name = ""
    label = ""
    color = ""
    onClick = ""
    modal = ""
    novaliade = False
    type = ""
    def __init__(self, name, label, color="primary", onClick="", modal="", formnovalidate=False, type="submit"):
        self.name = name
        self.label= label
        self.color = color
        self.onClick = onClick
        self.modal = modal
        self.novaliade = formnovalidate
        self.type = type
    def __str__(self):
        antwort ='<button class="btn btn-'+self.color+'" name="button" value="'+self.label+'" '
        antwort += 'type="'+self.type+'" '
        if self.onClick != "":
            antwort += ' onclick="'+self.onClick+'()" '
        if self.modal != "":
            antwort += 'data-toggle="modal" data-target="#'
            antwort += self.modal
            antwort += '" '
        if self.novaliade:
            antwort += " formnovalidate"
        antwort += ' >'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort
        
class FormBtnSave:
    name = "Speichern"
    def __str__(self):
        antwort ='<button type="submit" class="btn btn-primary" name="button" value="save">'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort

class FormBtnOk:
    name = "OK"
    def __str__(self):
        antwort ='<button type="submit" class="btn btn-primary" name="button" value="ok">'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort
        
class FormBtnCancel:
    name = "Abbruch"
    def __str__(self):
        antwort ='<button type="submit" class="btn btn-danger" name="button" value="cancel" formnovalidate>'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort

class FormBtnNext:
    name = "Speichern und Nächster"
    def __str__(self):
        antwort ='<button type="submit" class="btn btn-primary" name="button" value="next">'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort

class FormBtnRemove:
    name = "Löschen"
    def __str__(self):
        antwort ='<button type="submit" class="btn btn-danger" name="button" value="remove" formnovalidate>'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort

def formZeile(*liste):
    antwort = '<div class="form-row">\n'
    for element in liste:
        antwort += '<div class="col">' 
        antwort += str(element)
        antwort += '</div>'
    antwort += '\n</div>'
    return antwort

def formLinie():
    return "<hr />"

def formDate():
    def __init__(self, name, liste = False, daten=False, filter=False, value=0, aktiv=True, submit=False, label=True, leerzeile=False, onclick=False):
            self.liste = liste
            self.submit = submit
            self.label = label
            self.leerzeile = leerzeile
            self.onclick = onclick
            self.filter = filter
            self.daten = daten

            
