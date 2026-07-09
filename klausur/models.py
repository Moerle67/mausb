from datetime import date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import math

# Create your models here.
class Thema(models.Model):
    titel = models.CharField(("Titel"), max_length=250, primary_key=True)
    kommentar = models.TextField(("Kommentar"), blank=True, null=True)
    

    class Meta:
        verbose_name = ("Thema")
        verbose_name_plural = ("Themen")
        ordering = ['titel']
    
    def __str__(self):
        return self.titel

    #def get_absolute_url(self):
    #    return reverse("Thema_detail", kwargs={"pk": self.pk})


class Frage(models.Model):
    titel = models.CharField(("Thema"), max_length=250)
    inhalt = models.CharField("Überschrift", max_length=50, default="?")
    frage = models.TextField(("Frage"))
    musterantwort = models.TextField(("Musterantwort"), default ="")
    bild = models.ImageField(("Bild"), blank=True, null=True)
    bildmuster = models.ImageField(("Bild Muster"), blank=True, null=True)
    bildbreite = models.IntegerField(("Bildbreite in %"), default=80)
    thema = models.ForeignKey(Thema, verbose_name=("Thema"), on_delete=models.RESTRICT)
    punkte = models.IntegerField(("Erreichbare Punkte"), default=1)
#    platz = models.IntegerField(("Platz"), default=2)
    schwierigkeit = models.IntegerField(("Schwierigkeit") , default=2)
    author = models.ForeignKey(User, verbose_name="Autor", on_delete=models.RESTRICT)
    class Meta:
        verbose_name = ("Frage")
        verbose_name_plural = ("Fragen")
        ordering = ['thema', 'titel', ]

    def __str__(self):
        return f"{self.titel}/{self.inhalt} ({self.thema} ({self.punkte} Punkte); {self.author})"

    #def get_absolute_url(self):
    #    return reverse("Fragen_detail", kwargs={"pk": self.pk})
class Teilnehmer(models.Model):
    name = models.CharField(("Name"), max_length=250)
    info = models.TextField("Infos", blank=True, null=True)

    class Meta:
        verbose_name = "Teilnehmer"
        verbose_name_plural = "Teilnehmer"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Teilnehmer_detail", kwargs={"pk": self.pk})

class Gruppe(models.Model):
    name = models.CharField("Bezeichnung", max_length=50)
    teilnehmer = models.ManyToManyField(Teilnehmer, verbose_name="Teilnehmer")

    class Meta:
        verbose_name = ("Gruppe")
        verbose_name_plural = ("Gruppen")
        ordering = ['name']
        
    def __str__(self):
        return self.name

    #def get_absolute_url(self):
    #    return reverse("Gruppe_detail", kwargs={"pk": self.pk})
    
class Klausur(models.Model):
    titel = models.CharField(("Überschrift"), max_length=50)
    thema = models.CharField(("Thema"), max_length=50)
    termin = models.DateTimeField(("termin"), auto_now=False, auto_now_add=False)
    # gruppe = models.CharField(("Gruppe"), max_length=50)
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
