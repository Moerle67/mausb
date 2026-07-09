from django.db import models
from django.contrib.auth.models import User

from lehrplan.models import Ausbildungseinheit

# Create your models here.

class Frage(models.Model):
    titel = models.CharField(("Thema"), max_length=250)
    thema = models.ForeignKey(Ausbildungseinheit, verbose_name=("Ausbildungseinheit"), on_delete=models.RESTRICT)
    inhalt = models.CharField("Überschrift", max_length=50, default="?")
    frage = models.TextField(("Frage"))
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