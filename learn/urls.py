from django.urls import path


from .views import *

app_name = "learn"
    
urlpatterns = [
    path('bin', bin ,name='bin'),
    path('bin/<int:wert>', bin ,name='bin_wert'),

    path('bin_ueb/', bin_ueb ,name='bin_ueb'),
    path('bin_ueb/<int:wert>', bin_ueb ,name='bin_ueb_wert'),
    path('bin_ueb/<int:wert>/<int:ziel>', bin_ueb ,name='bin_ueb_ziel'),

    path('set_bit', set_bit ,name='set_bit'),
]