from django.contrib import admin
from import_export import resources  
from import_export.admin import ImportExportMixin
from .models import Ausbilder, Standort, Team, Beruf, Gruppe, Teilnehmer, TNAnmerkung, Raum, LaptopTN, AbwesendMA, Jourfixe, TN_rios
# Register your models here.

admin.site.register(Standort)
admin.site.register(Beruf)
# admin.site.register(Gruppe)
admin.site.register(Raum)
#admin.site.register(TN_rios)

# admin.site.register(Teilnehmer)


@admin.register(Gruppe)
class GruppAdmin(admin.ModelAdmin):
     list_display = ("name", "get_count",)
     list_filter = ['team', 'activ',]

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

@admin.register(LaptopTN)
class LaptopTNAdmin(admin.ModelAdmin):
    list_filter = ['tn__group', 'tn', 'number', 'ausgabe']
    search_fields = ['number', 'tn__name']

@admin.register(AbwesendMA)
class AbwesendMAAdmin(admin.ModelAdmin):
    list_filter = ['aubi', 'day', 'daytime']

@admin.register(Jourfixe)
class JourfixeAdmin(admin.ModelAdmin):
    list_filter = ['gruppe', 'date']

class TN_rios_ressorce(resources.ModelResource):
    class Meta:
        model = TN_rios
        fields = ('id', 'nachname', 'vorname', 'geburtstag', 'grundlage', 'zusatz','massnahme', 'start', 'ende')

@admin.register(TN_rios)
class TN_riosAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'vorname', 'nachname', 'massnahme', 'start', 'ende', )
    search_fields = ('nachname', 'vorname', 'massnahme',)
    list_filter = ('massnahme', 'start', 'ende', )
    import_order = ('name', 'vorname', )
    resource_classes = (TN_rios_ressorce, )
    import_id_fields = ['id', 'nachname', 'vorname', 'geburtstag', 'grundlage', 'zusatz','massnahme', 'start', 'ende',]