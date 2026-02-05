from django.contrib import admin

from .models import TNAnwesend, Sitzplan

# Register your models here.

@admin.register(TNAnwesend)
class TNAnmerkungAdmin(admin.ModelAdmin):
    list_filter = ['teilnehmer__group', 'teilnehmer', 'ausbilder', 'datum']
    search_fields = ['teilnehmer__name', 'comment']

@admin.register(Sitzplan)
class SitzplanAdmin(admin.ModelAdmin):
    list_filter = ['raum', 'teilnehmer']


