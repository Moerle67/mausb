from django.urls import path


from .views import start

app_name = "kklausur"
    
urlpatterns = [
    path('', start ,name='start'),
]