from django.urls import path


from .views import start

app_name = "fa"
    
urlpatterns = [
    path('', start ,name='start'),
]