from django.contrib import admin

from .models import Aufgabe, Bereich

# Register your models here.

# admin.site.register(Aufgabe)
admin.site.register(Bereich)


@admin.register(Aufgabe)
class AufgabeAdmin(admin.ModelAdmin):
    list_filter         = ['verantwortlich', 'aktuell', 'aktiv']
    search_fields = ['ueber', 'inhalt']