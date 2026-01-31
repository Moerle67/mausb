from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here

class Ausbilder(models.Model):
    user = models.OneToOneField(User, verbose_name=("SystemUser"), on_delete=models.RESTRICT)
    short = models.CharField(("Kürzel"), max_length=10)
    activ = models.BooleanField(("Aktiv"), default=True)
    bg_color = models.CharField(("Hintergrundfarbe"), max_length=50, default="DodgerBlue")
    fg_color = models.CharField("Schriftfarbe", max_length=50, default="white")
    comment = models.TextField(("Kommentar"), blank=True, null=True)

    class Meta:
        verbose_name = "Ausbilder"
        verbose_name_plural = "Ausbilder"

    def __str__(self):
        status = "Aktiv" if self.activ else "Inaktiv"
        return f"{self.user.first_name} {self.user.last_name} ({self.short}/{status})"

    def get_absolute_url(self):
        return reverse("Ausbilder_detail", kwargs={"pk": self.pk})

class Raum(models.Model):
    bezeichnung = models.CharField("Bezeichnung", max_length=10)
    info = models.TextField(("Info"))
    row = models.IntegerField(("Reihen"), default=5)
    col = models.IntegerField(("Spalten"), default=6)
    gang = models.IntegerField(("Gang"), default=3)
    
    class Meta:
        verbose_name = "Raum"
        verbose_name_plural = "Räume"

    def __str__(self):
        return f"{self.bezeichnung} - {self.info}"

    def get_absolute_url(self):
        return reverse("Raum_detail", kwargs={"pk": self.pk})

class Standort(models.Model):
    short = models.CharField(("Kürzel"), max_length=10)
    ort = models.CharField("Ort", max_length=50)
    description = models.TextField(("Beschreibung"), null=True, blank=True)
    activ = models.BooleanField("Aktiv", default=True)
    
    class Meta:
        verbose_name = "Standort"
        verbose_name_plural = "Standorte"

    def __str__(self):
        return f"{self.short} - {self.ort}"

    def get_absolute_url(self):
        return reverse("Standort_detail", kwargs={"pk": self.pk})

class Team(models.Model):
    name = models.CharField(("Bezeichnung"), max_length=50)
    short = models.CharField(("Kürzel"), max_length=10)
    aubi = models.ManyToManyField(Ausbilder, verbose_name=("Ausbilder"))
    standort = models.ForeignKey(Standort, verbose_name=("Standort"), on_delete=models.CASCADE)
    head = models.ForeignKey(Ausbilder, verbose_name=("Teamleiter"), related_name="Teamleiter", on_delete=models.RESTRICT, null=True, blank=True)
    activ = models.BooleanField(("aktiv"), default=True)

    class Meta:
        verbose_name = ("Team")
        verbose_name_plural = ("Teams")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Team_detail", kwargs={"pk": self.pk})

class Beruf(models.Model):
    short = models.CharField(("Kürzel"), max_length=10)
    name = models.CharField(("Bezeichnung"), max_length=50)
    activ = models.BooleanField(("Aktiv"), default=True)

    class Meta:
        verbose_name = "Beruf"
        verbose_name_plural = "Berufe"
        ordering = ["short"]

    def __str__(self):
        return f"{self.name} ({self.short})"

    def get_absolute_url(self):
        return reverse("Beruf_detail", kwargs={"pk": self.pk})


class Gruppe(models.Model):
    name = models.CharField("Name", max_length=50)
    short = models.CharField("Kürzel", max_length=10)
    speaker = models.ForeignKey('Teilnehmer', verbose_name=("Gruppensprecher"), on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(Team, verbose_name="Team", on_delete=models.RESTRICT)
    activ = models.BooleanField(("aktiv"), default=True)
    raum = models.ForeignKey(Raum, verbose_name="Raum", on_delete=models.RESTRICT, null = True, blank = True)

    class Meta:
        verbose_name = "Gruppe"
        verbose_name_plural = "Gruppen"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Gruppe_detail", kwargs={"pk": self.pk})

class Teilnehmer(models.Model):
    name = models.CharField("Name", max_length=50)
    profession = models.ForeignKey(Beruf, verbose_name=("Beruf"), on_delete=models.RESTRICT)
    group = models.ForeignKey(Gruppe, verbose_name=("Gruppe"), on_delete=models.CASCADE)
    activ = models.BooleanField(("aktiv"), default=True)

    class Meta:
        verbose_name = "Teilnehmer"
        verbose_name_plural = "Teilnehmer"
        ordering = ["group", "name"]

    def __str__(self):
        return f"{self.name} ({self.profession.short}/{self.group.short})"

    def get_absolute_url(self):
        return reverse("Teilnehmer_detail", kwargs={"pk": self.pk})
    
class TNAnmerkung(models.Model):
    teilnehmer = models.ForeignKey(Teilnehmer, verbose_name="Teilnehmer", on_delete=models.CASCADE)
    ausbilder = models.ForeignKey(Ausbilder, verbose_name="Ausbilder", on_delete=models.CASCADE)
    date = models.DateTimeField("Datum", auto_now=False, auto_now_add=True)
    comment = models.TextField("Anmerkung")

    class Meta:
        verbose_name = "TNAnmerkung"
        verbose_name_plural = "TNAnmerkungen"
        ordering = ['-date']

    def __str__(self):
        return f"{self.teilnehmer} - ({self.date}/{self.ausbilder.short}) {self.comment} " 

    def get_absolute_url(self):
        return reverse("TNAnmerkungen_detail", kwargs={"pk": self.pk})

