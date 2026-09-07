from django.urls import path


from .views import *

app_name = "klausur"
    
urlpatterns = [
    path('', start, name='start'),                                              # Start Klausuren Auswahl Gruppe
    path('ausw_klausur/<int:gruppe>', ausw_klausur, name='ausw_klausur'),       # Start 2 Auswahl Klausur
    path('new_klausur/<int:gruppe>', new_klausur, name='ausw_klausur'),         # Start 2 Auswahl Klausur
    path('detail_klausur/<int:klausur>', detail_klausur, name='detail_klausur'), # Start 2 Auswahl Klausur

    path('chg_klausur_title>', chg_klausur_title, name='chg_klausur_title'),   # Neuen Titel in Klausur speichern
    path('gen_pdf/<int:klausur>', gen_pdf, name='gen_pdf'),                     # PDF generieren     
]

