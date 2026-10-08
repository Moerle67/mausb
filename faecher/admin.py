from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Schrank)
# admin.site.register(Fach)

@admin.register(Fach)
class FachAdmin(admin.ModelAdmin):
    search_fields = ['user__name', 'number']
    list_display = ['schrank','number', 'user', 'belegtbis']
    list_filter = ['schrank', 'belegtbis']