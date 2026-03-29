from django.urls import path
from . import views

app_name = "task"

urlpatterns = [
    path('', views.start, name = "start"),                                  # Start ohne Paramter
    path('get_task_form', views.get_task_form, name = "get_task_form"),     # Daten für Formular add Task holen
    path('save_task_form', views.save_task_form, name = "save_task_form"),     # Daten für Formular add Task holen
        
]