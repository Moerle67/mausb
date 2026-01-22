from django.urls import path
from .views import start, anw_group, anw_detail, savedate

app_name = "anw"
    
urlpatterns = [
    path('', start ,name='start'),
    path('<int:id>', anw_group ,name='anw_g'),
    path('detail/<int:id>', anw_detail ,name='anw_detail'),
    path('detail/<int:id>/<str:aim_date>', savedate ,name='savedate_date'),    
    path('savedate', savedate ,name='savedate'),    
]