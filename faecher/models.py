from django.db import models
from django.urls import reverse

from stammdaten.models import Teilnehmer, Ausbilder

# Create your models here.

class Schrank(models.Model):
    bezeichnung = models.CharField("Bezeichnung", max_length=50, unique=True)
    hoehe       = models.IntegerField("Anzahl Höhe")
    breite      = models.IntegerField("Breite")
    start       = models.IntegerField("Start")

    class Meta:
        verbose_name = "Schrank"
        verbose_name_plural = "Schränke"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Schrank_detail", kwargs={"pk": self.pk})


class Fach(models.Model):
    user = models.ForeignKey(Teilnehmer, verbose_name="Benutzer", on_delete=models.RESTRICT)
    nummer = models.IntegerField("Fachnummer", unique=True)
    belegtbis = models.DateField("belegt bis:", auto_now=False, auto_now_add=False)
    eingetragen = models.DateTimeField("eingetragen am", auto_now=False, auto_now_add=True)
    eingetragenvon = models.ForeignKey(Ausbilder, verbose_name= "eingetragen von", on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "Fach"
        verbose_name_plural = "Fächer"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Fach_detail", kwargs={"pk": self.pk})

