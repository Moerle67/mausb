from django.urls import path
from .views import start, anw_group, anw_detail

app_name = "anw"
    
urlpatterns = [
    path('', start ,name='start'),
    path('<int:id>', anw_group ,name='anw_g'),
    path('detail/<int:id>', anw_detail ,name='anw_detail'),
]