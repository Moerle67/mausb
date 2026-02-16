from django.urls import path
from . import views

app_name = "ausbildungsplan"

urlpatterns = [
    path('', views.start, name = "start"),                      # Start ohne Paramter
    path('<int:team>', views.start, name = "team"),             # Start mit Team ID
    path('<int:team>/<str:date>', views.start, name = "date"),  # Start mit Team ID und Datum 'dd.mm.yyyy'
]