from django.urls import path
from . import views

app_name = "ausbildungsplan"

urlpatterns = [
    path('', views.start, name = "start"),                      # Start ohne Paramter
    path('<int:team>', views.start, name = "team"),             # Start mit Team ID
    path('<int:team>/<str:date>', views.start, name = "date"),  # Start mit Team ID und Datum 'dd.mm.yyyy'
    path('ausw_pp', views.ausw_pp, name = "ausw_pp"),           # Plug & Play neuer Block'
    path('rem_block', views.rem_block, name = "rem_block"),     # Block löschen
    path('save_content', views.save_content, name = "save_content"),     # Content speichern
    path('add_abwpp', views.add_abwpp, name = "add_abwpp"),     # Abwesende Mitarbeiter P&P

    path('del_le', views.del_le, name = "del_le"),              # Lerneinheit aus Block löschen
    path('save_le', views.save_le, name = "save_le"),           # Lerneinheit für Block speichern
]