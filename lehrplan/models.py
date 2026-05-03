from django.db import models
from django.urls import reverse
from django.db.models import Sum

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
        verbose_name_plural = ("RLP_01_Rahmenlehrpläne")

    def __str__(self):
        return f"{self.bereich} - {self.bundesland} vom {self.date}"

    def get_absolute_url(self):
        return reverse("Daytime_detail", kwargs={"pk": self.pk})
    
class Lernfeld(models.Model):
    rahmenlehrplan = models.ForeignKey(Rahmenlehrplan, verbose_name=("Rahmenlehrplan"), on_delete=models.RESTRICT)
    nummer = models.CharField(("Nummer"), max_length=50)
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
        # lst_block = Block.objects.filter(lernfeld=self)
        stunden = 0
#        for block in lst_block:
#            stunden += block.laenge
        return stunden

    @property
    def get_berufe(self):
        berufe = ""
        lst_berufe = self.berufe.all()
        for beruf in lst_berufe:
            berufe += beruf.short + " / "
        return berufe[:-2]   
         
    class Meta:
        verbose_name = ("Lernfeld")
        verbose_name_plural = ("RLP_02_Lernfelder")
        ordering = ["rahmenlehrplan", "nummer"]
         

    def __str__(self):
        return f"{self.nummer} {self.inhalt} {self.get_berufe} ({self.get_block_stunden}/{self.get_stunden} Stunden)"

    def get_absolute_url(self):
        return reverse("Lernfeld_detail", kwargs={"pk": self.pk})

class Fachrichtung(models.Model):
    fachrichtung = models.CharField("Fachrichtung", max_length=50)
    short = models.CharField(("Kürzel"), max_length=5)
    details = models.TextField(("Details"), null = True, blank = True)
    
    class Meta:
        verbose_name = "Fachrichtung"
        verbose_name_plural = "LE_01_Fachrichtungen"

    @property
    def get_aubi_set(self):
        aubi_set = set([])
        lst_themen = Thema.objects.filter(fachrichtung = self)
        for thema in lst_themen:
            aubi_set |= thema.get_aubi_set
        return aubi_set

    @property
    def get_aubi(self):
        return  ", ".join([i.user.last_name for i in self.get_aubi_set])

    @property
    def get_sum(self):
        lst_themen = Thema.objects.filter(fachrichtung = self)
        summe = 0
        for thema in lst_themen:
            if thema.get_sum:
                summe += thema.get_sum
        return summe

    def __str__(self):
        return f"{self.fachrichtung} ({self.get_sum} UE) - {self.get_aubi}"

    def get_absolute_url(self):
        return reverse("Fachrichtung_detail", kwargs={"pk": self.pk})

class Thema(models.Model):
    thema = models.CharField("Thema", max_length=50)
    short = models.CharField(("Kürzel"), max_length=5)
    fachrichtung = models.ForeignKey(Fachrichtung, verbose_name="Fachrichtung", on_delete=models.CASCADE)
    berufe = models.ManyToManyField(Beruf, verbose_name = "")
    details = models.TextField(("Details"), null = True, blank = True)

    class Meta:
        verbose_name = "Thema"
        verbose_name_plural = "LE_02_Themen"

    @property
    def get_aubi_set(self):
        lst_aubi = set([])
        lst_le = Lerneinheit.objects.filter(thema = self)
        for le in lst_le:
            lst_aubi |= set(list(le.ausbilder.filter(activ=True)))
        return lst_aubi

    @property
    def get_aubi(self):
        menge = self.get_aubi_set
        return  ", ".join([i.user.last_name for i in menge])

    @property
    def get_sum(self):
        return Lerneinheit.objects.filter(thema = self).aggregate(Sum("time"))['time__sum']

    def __str__(self):
        return f"{self.thema} ({self.fachrichtung.short} ({self.get_sum})) - {self.get_aubi}"

    def get_absolute_url(self):
        return reverse("Thema_detail", kwargs={"pk": self.pk})

class Lerneinheit(models.Model):
    thema = models.ForeignKey(Thema, verbose_name=("Thema"), on_delete=models.CASCADE)
    inhalt = models.CharField("Inhalt", max_length=50)
    beschreibung = models.TextField("Beschreibung")
    information = models.URLField(("Wiki-Link"), max_length=200, blank = True, null = True)
    ausbilder = models.ManyToManyField(Ausbilder, verbose_name=("Ausbilder"))
    time = models.IntegerField("Anzahl Unterrichtseinheiten", default=5)
    lernfeld = models.ManyToManyField(Lernfeld, verbose_name="entsprechende Lernfelder", blank = True)

    class Meta:
        verbose_name = "Lerneinheit"
        verbose_name_plural = "LE_03_Lerneinheiten"
        ordering = ['thema', 'inhalt']  

    @property
    def get_aubi(self):
        lst_aubi = list(self.ausbilder.filter(activ = True))
        antwort = ", ".join([i.user.last_name for i in lst_aubi])
        return antwort   

    def __str__(self):
        return f"{self.inhalt} {self.time} UE/{self.get_aubi} ({self.thema.short})"

    def get_absolute_url(self):
        return reverse("Lerneinheit_detail", kwargs={"pk": self.pk})

class Ausbildungseinheit(models.Model):
    thema = models.ForeignKey("Ausbildungseinheit", verbose_name=("Thema"), on_delete=models.CASCADE, blank = True, null = True)
    inhalt = models.CharField("Inhalt", max_length=50)
    beschreibung = models.TextField("Beschreibung")
    information = models.URLField(("Wiki-Link"), max_length=200, blank = True, null = True)
    ausbilder = models.ManyToManyField(Ausbilder, verbose_name=("Ausbilder"), blank=True)
    time = models.IntegerField("Anzahl Unterrichtseinheiten", default=5)
    lernfeld = models.ManyToManyField(Lernfeld, verbose_name="entsprechende Lernfelder", blank = True)

    class Meta:
        verbose_name = "Ausbildungseinheit"
        verbose_name_plural = "Ausbildungseinheiten"
        ordering = ['inhalt']  

    @property
    def get_aubi(self):
        lst_aubi = list(self.ausbilder.filter(activ = True))
        antwort = ", ".join([i.user.last_name for i in lst_aubi])
        return antwort   

    @property
    def get_time(self):
        sum_direkt = Ausbildungseinheit.objects.filter(thema=self).aggregate(Sum("time"))['time__sum']
        sum_direkt = sum_direkt if sum_direkt else 0
        sum_rekursiv = 0
        lst_children = Ausbildungseinheit.objects.filter(thema=self)
        for element in lst_children:
            sum_rekursiv += element.get_time if element.get_time else 0
        return sum_direkt + sum_rekursiv
    
    def __str__(self):
        thema = self.thema.inhalt if self.thema != None else ""
        return f"{self.inhalt} {self.time}/{self.get_time} UE/{self.get_aubi} ({thema})"

    def get_absolute_url(self):
        return reverse("Lerneinheit_detail", kwargs={"pk": self.pk})
