from datetime import date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import math

from lehrplan.models import Ausbildungseinheit
from stammdaten.models import Gruppe, Teilnehmer

# Create your models here.

class Frage(models.Model):
    titel = models.CharField(("Thema intern"), max_length=250)
    inhalt = models.CharField("Überschrift", max_length=50, default="?")
    frage = models.TextField(("Frage"))
    musterantwort = models.TextField(("Musterantwort"), default ="")
    bild = models.ImageField(("Bild"), blank=True, null=True)
    bildmuster = models.ImageField(("Bild Muster"), blank=True, null=True)
    bildbreite = models.IntegerField(("Bildbreite in %"), default=80)
    thema = models.ForeignKey(Ausbildungseinheit, verbose_name=("Thema"), on_delete=models.RESTRICT)
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
    titel = models.CharField(("Überschrift"), max_length=50)
    thema = models.CharField(("Thema"), max_length=50)
    termin = models.DateTimeField(("termin"), auto_now=False, auto_now_add=False)
    gruppe = models.ForeignKey(Gruppe, verbose_name=("Gruppe"), on_delete=models.CASCADE, null=True)
    fragen = models.ManyToManyField(Frage, verbose_name=("Fragen"))
    author = models.ForeignKey(User, verbose_name="Autor", on_delete=models.RESTRICT)

    @property
    def get_gesamtpunkte(self):
        fragen = self.fragen.all()
        gesamtpunkte = sum(frage.punkte for frage in fragen)
        return gesamtpunkte

    @property
    def get_aktiv(self):
        if self.termin > date.today():
            return True
        else:
            return False
            
    class Meta:
        verbose_name = ("Klausur")
        verbose_name_plural = ("Klausuren")
        ordering = [ 'gruppe', '-termin']

    def __str__(self):
        return f"{self.gruppe} - {self.titel}/{self.termin.date()}/{self.get_gesamtpunkte} Punkte, {self.author}" 

    #def get_absolute_url(self):
    #    return reverse("klausur_design", kwargs={"pk": self.pk})
    
class Klausurthema(models.Model):
    klausur = models.ForeignKey(Klausur, verbose_name=("Klausur"), on_delete=models.CASCADE)
    frage = models.ForeignKey(Frage, verbose_name=("Frage"), on_delete=models.RESTRICT)
    position = models.IntegerField(("Position"), default=10)
    seitenwechsel = models.BooleanField(("Seitenwechsel im Anschluss"), default=False)
    class Meta:
        verbose_name = ("Klausur-Thema")
        verbose_name_plural = ("Klausur-Themen")
        ordering = ['klausur', 'position']

    def __str__(self):
        return f"{self.klausur}/{self.frage}({self.frage.punkte} Punkte)"

    #def get_absolute_url(self):
    #    return reverse("KlausurThema_detail", kwargs={"pk": self.pk})

class Answer(models.Model):
    teilnehmer = models.ForeignKey(Teilnehmer, verbose_name="Teilnhmer*in", on_delete=models.CASCADE)
    klausur = models.ForeignKey(Klausur, verbose_name="Klausur", on_delete=models.CASCADE)
    frage = models.ForeignKey(Frage, verbose_name="Frage", on_delete=models.CASCADE)
    punkte = models.IntegerField(("Punkte"), default=0)
    bemerkung = models.TextField(("Bemerkung"), blank=True, null=True)
    

    @property
    def get_gesamtpunkte(self, teilnehmer, klausur): 
        punkte = self.filter(teilnehmer = teilnehmer, klausur = klausur).sum()
        return punkte

    class Meta:
        verbose_name = "Antwort"
        verbose_name_plural = "Antworten"

    def __str__(self):
        return f"{self.frage} - {self.teilnehmer} ({self.punkte}/{self.frage.punkte})"

    def get_absolute_url(self):
        return reverse("Solution_detail", kwargs={"pk": self.pk})

class Bewertung(models.Model):
    note = models.IntegerField(("Note"))
    bewertung =models.CharField(("Bewertung"), max_length=50)

    class Meta:
        verbose_name = ("Bewertung")
        verbose_name_plural = ("Bewertungen")

    def __str__(self):
        return f"{self.note} - {self.bewertung}"

    def get_absolute_url(self):
        return reverse("Bewertung_detail", kwargs={"pk": self.pk})

class IHK_key(models.Model):
    punkte = models.IntegerField(("Punkte/Prozent"))
    note = models.FloatField(("Note"))

    @property
    def get_bewertung(self):
        note = round(self.note,0)
        return Bewertung.objects.get(note=note).bewertung


    class Meta:
        verbose_name = "IHK Notenschlüssel"
        verbose_name_plural = "IHK Notenschlüssel"
        ordering = ['-punkte']

    def __str__(self):
        return f"{self.punkte} / {self.note}"

    def get_absolute_url(self):
        return reverse("IHK_key_detail", kwargs={"pk": self.pk})
