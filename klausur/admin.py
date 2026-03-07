from django.contrib import admin

from .models import Klausur, Frage

# Register your models here.

admin.site.register(Klausur)
admin.site.register(Frage)