from django.urls import path
from .views import start, user_login, user_logout

app_name = "stammdaten"

urlpatterns = [
    path('', start ,name='start'),

    path('login', user_login, name="login"),                                                                                  # Login
    path('logout', user_logout, name="logout"),      
]
