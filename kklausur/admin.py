from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Frage)
admin.site.register(Klausur)
# admin.site.register(KlausurFrage)

@admin.register(KlausurFrage)
class KlausurFrageAdmin(admin.ModelAdmin):
    list_filter = ['klausur']