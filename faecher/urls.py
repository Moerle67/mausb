from django.urls import path

from .views import *

app_name = "faecher"
    
urlpatterns = [
    path('start',start ,name='start'),
    path('start/<int:schrank>',start ,name='start_nr'),

]