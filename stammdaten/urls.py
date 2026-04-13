from django.urls import path
from .views import start, user_login, user_logout, task, ajax_login

app_name = "stammdaten"

urlpatterns = [
    path('', start, name='start'),
    path('task', task, name='task'),

    path('login', user_login, name="login"),                                                                                  # Login
    path('logout', user_logout, name="logout"), 

    path('ajax_login', ajax_login, name="ajax_login"), 

]
