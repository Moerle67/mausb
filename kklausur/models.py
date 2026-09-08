from django.contrib.auth.models import User
from django.db import models

from lehrplan.models import Ausbildungseinheit
from stammdaten.models import Gruppe

# Create your models here.

class Frage(models.Model):
    titel = models.CharField(("Thema"), max_length=250)
    thema = models.ForeignKey(Ausbildungseinheit, verbose_name=("Ausbildungseinheit"), on_delete=models.RESTRICT)
    inhalt = models.CharField("Überschrift", max_length=50, default="?")
    frage = models.TextField("Frage")
    musterantwort = models.TextField(("Musterantwort"), default ="")
    bild = models.ImageField(("Bild"), blank=True, null=True)
    bildmuster = models.ImageField(("Bild Muster"), blank=True, null=True)
    bildbreite = models.IntegerField(("Bildbreite in %"), default=80)
    punkte = models.IntegerField(("Erreichbare Punkte"), default=1)
    author = models.ForeignKey(User, verbose_name="Autor", on_delete=models.RESTRICT)
    
    class Meta:
        verbose_name = ("Frage")
        verbose_name_plural = ("Fragen")
        ordering = ['thema', 'titel', ]

    def __str__(self):
        return f"{self.titel}/{self.inhalt} ({self.thema} ({self.punkte} Punkte); {self.author})"

    #def get_absolute_url(self):
    #    return reverse("Fragen_detail", kwargs={"pk": self.pk})

class Klausur(models.Model):
    title       = models.CharField(("Überschrift"), max_length=50)
    gruppe      = models.ForeignKey(Gruppe, verbose_name="Gruppe", on_delete=models.CASCADE)
    thema       = models.ForeignKey(Ausbildungseinheit, verbose_name="Thema", on_delete=models.SET_NULL, null=True)
    datum       = models.DateTimeField("Termin", auto_now=False, auto_now_add=False)
    erledigt    = models.BooleanField("abgeschlossen", default = False)
    comment     = models.TextField("Kommentar", blank=True, null=True)

    class Meta:
        verbose_name            = "Klausur"
        verbose_name_plural     = "Klausuren" 
        ordering                = ["gruppe", "-datum"]

    def __str__(self):
        return f"{self.gruppe} / {self.title} ({self.datum.date()})"

    @property
    def get_gesamtpunkte(self):
        kfragen = KlausurFrage.objects.filter(klausur = self)
        return sum(frage.frage.punkte for frage in kfragen)
    
    #    def get_absolute_url(self):
    #        return reverse("Klausur_detail", kwargs={"pk": self.pk})
    
class KlausurFrage(models.Model):
    klausur     = models.ForeignKey(Klausur, verbose_name="Klausur", on_delete=models.CASCADE)
    frage       = models.ForeignKey(Frage, verbose_name="Frage", on_delete=models.CASCADE)
    position    = models.IntegerField("Position", default=0)
    startnp     = models.BooleanField("Start mit neuer Seite", default=False)

    class Meta:
        verbose_name        = "KlausurFrage"
        verbose_name_plural = "KlausurFrage"
        ordering            = ["klausur", "position"]

    def __str__(self):
        return f"{self.klausur} - {self.frage} ({self.position})"

    @property
    def get_erledigt(self):
        return self.klausur.erledigt  

    #def get_absolute_url(self):
    #    return reverse("KlausurFrage_detail", kwargs={"pk": self.pk})
    