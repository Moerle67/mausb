from django.db import models
from django.urls import reverse

from stammdaten.models import Teilnehmer
# Create your models here.

class Tn_fa(models.Model):
    teilnehmer = models.ForeignKey(Teilnehmer, verbose_name="Teilnehmer", on_delete=models.CASCADE)
    datum = models.DateTimeField("Datum", auto_now=False, auto_now_add=True)
    status = models.IntegerField("Status")
    comment = models.TextField("Kommentar", null=True, blank=True)

    class Meta:
        verbose_name = "Teilnehmer Frage/Anwort"
        verbose_name_plural = "Teilnehmer Fragen/Anworten"
        ordering = ['-datum']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tn_fa_detail", kwargs={"pk": self.pk})

