from django.urls import path


from .views import *

app_name = "klausur"
    
urlpatterns = [
    path('', start, name='start'),                                              # Start Klausuren Auswahl Gruppe
    path('ausw_klausur/<int:gruppe>', ausw_klausur, name='ausw_klausur'),       # Start 2 Auswahl Klausur
    path('new_klausur/<int:gruppe>', new_klausur, name='ausw_klausur'),         # Start 2 Auswahl Klausur
    path('add_klas/<int:team>', add_klas, name='add_klas'),                     # Klausur zufügen
    path('gen_pdf/<int:klausur>', gen_pdf, name='gen_pdf'),                     # PDF generieren     
]

