from django.urls import path


from .views import *

app_name = "kklausur"
    
urlpatterns = [
    path('', start ,name='start'),                  # Start Klausuren
    path('add_klas/<int:team>', add_klas, name='add_klas'),   # Klausur zufügen 
]

