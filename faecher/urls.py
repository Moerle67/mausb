from django.urls import path

from .views import *

app_name = "faecher"
    
urlpatterns = [
    path('',start ,name='start'),
    path('<int:schrank>', start, name='start_nr'),
    
    path('get_fach', get_fach, name='get_fach'),

]