from django.contrib import admin

from .models import Rahmenlehrplan, Lernfeld, Fachrichtung, Thema, Lerneinheit

# Register your models here.

admin.site.register(Rahmenlehrplan)
# admin.site.register(Lernfeld)
admin.site.register(Fachrichtung)
admin.site.register(Thema)
# admin.site.register(Lerneinheit)

@admin.register(Lerneinheit)
class TeamAdmin(admin.ModelAdmin):
    filter_horizontal   = ['ausbilder', 'lernfeld']
    list_filter         = ['thema']

@admin.register(Lernfeld)
class LernfeldAdmin(admin.ModelAdmin):
       filter_horizontal   = ['berufe']