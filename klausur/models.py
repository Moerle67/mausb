from django.db import models
from django.urls import reverse


from stammdaten.models import Gruppe

from lehrplan.models import Thema

# Create your models here.

class Klausur(models.Model):
    gruppe = models.ForeignKey(Gruppe, verbose_name = "Gruppe", on_delete=models.CASCADE)
    thema = models.ForeignKey(Thema, verbose_name = "Thema", on_delete=models.CASCADE)
    name = models.CharField("Überschrift", max_length=50)
    zeitpunkt = models.DateTimeField("Zeitpunkt", auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "Klausur"
        verbose_name_plural = "Klausuren"

    def __str__(self):
        return f"{self.name} - {self.thema} ({self.gruppe.short}/{self.zeitpunkt})"

    def get_absolute_url(self):
        return reverse("Klausur_detail", kwargs={"pk": self.pk})

class Frage(models.Model):
    name = models.CharField("Titel", max_length=50)
    thema = models.ForeignKey(Thema, verbose_name=("Thema"), on_delete=models.CASCADE)
    frage = models.TextField("Frage")
    antwort = models.TextField("Musterantwort")
    bild = models.ImageField("Abbildung", upload_to="kimage", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    punkte = models.IntegerField(("Anzahl Punkte"), default = 1)

    class Meta:
        verbose_name = "Frage"
        verbose_name_plural = "Fragen"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Frage_detail", kwargs={"pk": self.pk})
