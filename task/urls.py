from django.urls import path
from . import views

app_name = "task"

urlpatterns = [
    path('', views.start, name = "start"),                                  # Start ohne Paramter
    path('get_task_form', views.get_task_form, name = "get_task_form"),     # Daten für Formular add Task holen
    path('save_task_form', views.save_task_form, name = "save_task_form"),  # Daten für Formular add Task holen
    path('task_dnd', views.task_dnd, name = "task_dnd"),                    # Daten für Formular add Task holen
    path('get_task', views.get_task, name = "get_task"),                    # Task an Front-End schicken
    path('del_task', views.del_task, name = "del_task"),                    # Daten für Formular add Task holen
        
]