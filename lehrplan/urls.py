from django.urls import path
from . import views

app_name = "inh"

urlpatterns = [
    path('', views.start, name = "start"),                      # Start ohne Paramter    
]