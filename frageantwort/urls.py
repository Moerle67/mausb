from django.urls import path


from .views import *

app_name = "fa"
    
urlpatterns = [
    path('<int:gruppe>', start, name='start'),
    path('svtn', savetn, name='savetn'),
    path('newlst', newlst, name='newlst'),
    path('get_tn', get_tn, name='get_tn'),  
]