from django.urls import path
from .views import start, anw_group, anw_detail, savedate, anw_note

app_name = "anw"
    
urlpatterns = [
    path('', start ,name='start'),
    path('<int:id>', anw_group ,name='anw_g'),
    path('detail/<int:id>', anw_detail ,name='anw_detail'),
    path('detail/<int:id>/<str:aim_date>', anw_detail ,name='savedate_date'), 
    path('detail_tnnote/', anw_note, name='anw_note'), 
    path('savedate', savedate ,name='savedate'),    
]