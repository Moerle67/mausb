from django.db import models
from django.urls import reverse

from stammdaten.models import Beruf, Ausbilder

# Create your models here.

class Rahmenlehrplan(models.Model):
    date = models.DateField("Version von")
    bereich = models.CharField("Bereich", max_length=50)
    description = models.TextField(("Beschreibung"), blank=True, null=True)
    bundesland = models.CharField(("Beschreibung"), max_length=50, default="Baden-Württemberg")
    quelle = models.URLField("Quelle", max_length=200)
    aktiv = models.BooleanField(("aktiv"), default=True)

    class Meta:
        verbose_name = ("Rahmenlehrplan")
        verbose_name_plural = ("Rahmenlehrpläne")

    def __str__(self):
        return f"{self.bereich} - {self.bundesland} vom {self.date}"

    def get_absolute_url(self):
        return reverse("Daytime_detail", kwargs={"pk": self.pk})
    
class Lernfeld(models.Model):
    rahmenlehrplan = models.ForeignKey(Rahmenlehrplan, verbose_name=("Rahmenlehrplan"), on_delete=models.RESTRICT)
    nummer = models.CharField(("Nummer"), max_length=5)
    inhalt = models.CharField(("Inhalt"), max_length=200)
    stunden1 = models.IntegerField(("Zeitrichtwerte 1. Jahr"), default = 0)
    stunden2 = models.IntegerField(("Zeitrichtwerte 2. Jahr"), default = 0)
    stunden3 = models.IntegerField(("Zeitrichtwerte 3. Jahr"), default = 0)
    berufe = models.ManyToManyField(Beruf, verbose_name=("Berufe"))
    beschreibung = models.TextField(("Beschreibung"))


    @property
    def get_stunden(self):
        return self.stunden1 + self.stunden2 + self.stunden3
    
    @property
    def get_block_stunden(self):
        lst_block = Block.objects.filter(lernfeld=self)
        stunden = 0
        for block in lst_block:
            stunden += block.laenge
        return stunden

    @property
    def get_berufe(self):
        berufe = ""
        lst_berufe = self.berufe.all()
        for beruf in lst_berufe:
            berufe += beruf.kuerzel + " / "
        return berufe[:-2]   
         
    class Meta:
        verbose_name = ("Lernfeld")
        verbose_name_plural = ("Lernfelder")
        ordering = ["rahmenlehrplan", "nummer"]
        
    def __str__(self):
        return f"{self.nummer} {self.inhalt} {self.get_berufe} ({self.get_block_stunden}/{self.get_stunden} Stunden)"

    def get_absolute_url(self):
        return reverse("Lernfeld_detail", kwargs={"pk": self.pk})

class Fachrichtung(models.Model):
    fachrichtung = models.CharField("Fachrichtung", max_length=50)
    details = models.TextField(("Details"), null = True, blank = True)
    
    class Meta:
        verbose_name = _("Fachrichtung")
        verbose_name_plural = _("Fachrichtungen")

    def __str__(self):
        return self.fachrichtung

    def get_absolute_url(self):
        return reverse("Fachrichtung_detail", kwargs={"pk": self.pk})

class Thema(models.Model):
    thema = models.CharField("Thema", max_length=50)
    fachrichtung = models.ForeignKey(Fachrichtung, verbose_name="Fachrichtung", on_delete=models.CASCADE)
    berufe = models.ManyToManyField(Beruf, verbose_name = "")
    details = models.TextField(("Details"), null = True, blank = True)

    class Meta:
        verbose_name = "Thema"
        verbose_name_plural = "Themen"

    def __str__(self):
        return f"{self.thema} ({self.fachrichtung})"

    def get_absolute_url(self):
        return reverse("Thema_detail", kwargs={"pk": self.pk})

class Lerneinheit(models.Model):
    thema = models.ForeignKey(Thema, verbose_name=("Thema"), on_delete=models.CASCADE)
    inhalt = models.CharField("Inhalt", max_length=50)
    beschreibung = models.TextField("Beschreibung")
    information = models.URLField(("Wiki-Link"), max_length=200, blank = True, null = True)
    planung = models.ForeignKey(Ausbilder, verbose_name="verantwortlich", on_delete=models.CASCADE)
    time = models.IntegerField("Anzahl Unterrichtseinheiten", default=5)
    lernfeld = models.ManyToManyField(Lernfeld, verbose_name="entsprechende Lernfelder", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lerneinheit"
        verbose_name_plural = "Lerneinheiten"   

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Lerneinheit_detail", kwargs={"pk": self.pk})
