from django.urls import path
from . import views

app_name = "inh"

urlpatterns = [
    path('', views.start, name = "start"),                      # Start ohne Paramter   
    path('start2', views.start2, name = "start2"),                      # Start Alternative   
     
]