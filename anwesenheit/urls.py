from django.urls import path


from .views import start, anw_group, anw_detail, savedate, anw_note, anw_raum, saveplan, delplan, savedateplan

app_name = "anw"
    
urlpatterns = [
    path('', start ,name='start'),
    path('<int:id>', anw_group ,name='anw_g'),
    path('detail/<int:id>', anw_detail ,name='anw_detail'),
    path('detail/<int:id>/<str:aim_date>', anw_detail ,name='savedate_date'), 
    path('raum/<int:group>/<str:date>', anw_raum ,name='anw_raum'), 
    path('detail_tnnote/', anw_note, name='anw_note'), 
    path('savedate', savedate, name='savedate'),
    path('savedateplan', savedateplan, name='savedateplan'),

    path('saveplan', saveplan, name='saveplan'),
    path('delplan', delplan, name='delplan'),
]