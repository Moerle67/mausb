from django.contrib import admin

from .models import Ausbilder, Standort, Team, Beruf
# Register your models here.

admin.site.register(Standort)
admin.site.register(Beruf)

@admin.register(Ausbilder)
class AusbilderAdmin(admin.ModelAdmin):
    list_filter = ['activ']
#    search_fields = ['user_name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ['aubi']