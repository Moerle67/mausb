from django.db import models
from stammdaten.models import Ausbilder, Teilnehmer, Raum, Gruppe
from django.urls import reverse

# Create your models here.
class Daytime(models.Model):
    short = models.CharField(("Kürzel"), max_length=2)
    long = models.CharField(("Langversion"), max_length=50)
    description = models.CharField(("Beschreibung"), max_length=50, null= True, blank=True)

    class Meta:
        verbose_name = ("Tageszeit")
        verbose_name_plural = ("Tageszeiten")

    def __str__(self):
        return f"{self.short}/{self.description}"

    def get_absolute_url(self):
        return reverse("Daytime_detail", kwargs={"pk": self.pk})

class Block(models.Model):
    group = models.ForeignKey(Gruppe, verbose_name=("Gruppe"), on_delete=models.CASCADE)
    date = models.DateField(("Datum"), auto_now=False, auto_now_add=False)
    daytime = models.ForeignKey(Daytime, verbose_name="Tageszeit", on_delete=models.RESTRICT)
    teacher = models.ForeignKey(Ausbilder, verbose_name=("Ausbilder"), on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(("Info"), max_length=50, null=True, blank=True)
    # lehrblock = models.ForeignKey(Lehrblock, verbose_name=("Ausbildungseinheit"), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = ("Block")
        verbose_name_plural = ("Blöcke")
        ordering = ["group", "date", "daytime"]

    def __str__(self):
        return f"{self.group.short} - {self.date}/{self.daytime.description} - {'' if self.teacher is None else self.teacher.user.last_name}"

    def get_absolute_url(self):
        return reverse("Block_detail", kwargs={"pk": self.pk})