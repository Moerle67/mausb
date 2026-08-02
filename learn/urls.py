from django.urls import path


from .views import *

app_name = "learn"
    
urlpatterns = [
    path('bin', bin ,name='bin'),
]