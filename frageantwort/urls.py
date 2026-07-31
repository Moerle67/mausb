from django.urls import path


from .views import start, savetn

app_name = "fa"
    
urlpatterns = [
    path('<int:gruppe>', start, name='start'),
    path('svtn', savetn, name='savetn'),
]