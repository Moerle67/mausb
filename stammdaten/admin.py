from django.contrib import admin

from .models import Ausbilder, Standort
# Register your models here.

admin.site.register(Standort)

@admin.register(Ausbilder)
class AusbilderAdmin(admin.ModelAdmin):
    list_filter = ['activ']
#    search_fields = ['user_name']