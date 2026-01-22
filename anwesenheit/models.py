from django.db import models

from stammdaten.models import Ausbilder, Teilnehmer


# Create your models here.

class TNAnwesend(models.Model):
    teilnehmer = models.ForeignKey(Teilnehmer, verbose_name="Teilnehmer", on_delete=models.CASCADE)
    ausbilder = models.ForeignKey(Ausbilder, verbose_name="Ausbilder", on_delete=models.CASCADE)
    datum = models.DateTimeField("Datum", auto_now=False, auto_now_add=True)
    anwesend = models.BooleanField("Anwesend")
    comment = models.TextField(("Kommentar"), null=True, blank=True)

    class Meta:
        verbose_name = "Teilnehmer Anwesenheit"
        verbose_name_plural = "Teilnehmer Anwesenheiten"
        ordering = ['teilnehmer', '-datum']

    def __str__(self):
        return f"{self.teilnehmer} {self.anwesend}/{self.datum}"

    def get_absolute_url(self):
        return reverse("TNAnwesend_detail", kwargs={"pk": self.pk})

