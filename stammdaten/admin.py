from django.contrib import admin

from .models import Ausbilder, Standort, Team, Beruf, Gruppe, Teilnehmer, TNAnmerkung
# Register your models here.

admin.site.register(Standort)
admin.site.register(Beruf)
admin.site.register(Gruppe)
# admin.site.register(Teilnehmer)


@admin.register(Ausbilder)
class AusbilderAdmin(admin.ModelAdmin):
    list_filter = ['activ']
#    search_fields = ['user_name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ['aubi']

@admin.register(Teilnehmer)
class TeilnehmerAdmin(admin.ModelAdmin):
    list_filter = ['group__team', 'group', 'profession', 'activ']
    search_fields = ['name']

@admin.register(TNAnmerkung)
class TNAnmerkungAdmin(admin.ModelAdmin):
    list_filter = ['teilnehmer__group', 'teilnehmer', 'ausbilder']
    search_fields = ['teilnehmer__name', 'comment']    