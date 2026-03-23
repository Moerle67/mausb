from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.urls import reverse

class Bereich(models.Model):
    name = models.CharField("Bezeichnung", max_length=50)
    beschreibung = models.TextField("Beschreibung")

    class Meta:
        verbose_name = "Bereich"
        verbose_name_plural = "Bereiche"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Bereich_detail", kwargs={"pk": self.pk})

class Aufgabe(models.Model):

    ueber = models.CharField(("Aufgabe"), max_length=50)
    bereich = models.ForeignKey(Bereich, verbose_name="Bereich", on_delete=models.CASCADE)
    inhalt = models.TextField("Inhalt")
    ersteller = models.ForeignKey(User, verbose_name="Erstellt von", on_delete=models.CASCADE, related_name="ersteller")
    verantwortlich = models.ForeignKey(User, verbose_name="verantwortlich", on_delete=models.CASCADE, related_name="responce")
    parent = models.ForeignKey('Aufgabe', verbose_name=("Ursprungsaufgabe"), on_delete=models.CASCADE, blank=True, null=True)
    prio = models.IntegerField("Priorität", default = 1)
    termin = models.DateTimeField("Termin", auto_now=False, auto_now_add=False, null=True, blank=True)
    created = models.DateTimeField("Erstellt", auto_now=False, auto_now_add=True)
    changed = models.DateTimeField("Geändert", auto_now=True, auto_now_add=False)
    aktuell = models.BooleanField(("wird aktuell bearbeitet"), default=False)
    zyklisch = models.BooleanField("wiederholt sich die Aufgabe?", default=False)
    aktiv = models.BooleanField(("Aktiv (offen)"), default=True)

    class Meta:
        verbose_name = "Aufgabe"
        verbose_name_plural = "Aufgaben"

    def __str__(self):
        return f"{self.ueber} / {self.verantwortlich}"

    def get_absolute_url(self):
        return reverse("Aufgabe_detail", kwargs={"pk": self.pk})

