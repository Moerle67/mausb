from django.urls import path
from .views import start

app_name = "anw"
    
urlpatterns = [
    path('', start ,name='start'),
]