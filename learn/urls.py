from django.urls import path


from .views import *

app_name = "learn"
    
urlpatterns = [
    path('bin', bin ,name='bin'),
    path('bin/<int:wert>', bin ,name='bin_wert'),
    path('set_bit', set_bit ,name='set_bit'),
]