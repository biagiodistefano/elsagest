from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from datetime import date, timedelta


# Create your models here.


class SezioneElsa(models.Model):
    nome = models.TextField()
    users = models.ManyToManyField(User)
    history = HistoricalRecords()

    class Meta:
        db_table = "sezioni_elsa"
        verbose_name = "Sezione ELSA"
        verbose_name_plural = "Sezioni ELSA"

    def __str__(self):
        return f"ELSA {self.nome}"


class Consigliere(models.Model):
    ruolo = models.TextField()

    class Meta:
        db_table = "ruoli_consiglieri"
        verbose_name = "Consigliere"
        verbose_name_plural = "Consiglieri"


class SociManager(models.Manager):

    def in_scadenza(self):
        return self.get_queryset().filter(scadenza_iscrizione__lte=date.today() + timedelta(days=15))

    def scaduto(self):
        return self.get_queryset().filter(scadenza_iscrizione__lte=date.today())


class Socio(models.Model):
    nome = models.TextField()
    cognome = models.TextField()
    sezione = models.ForeignKey(SezioneElsa, on_delete=models.CASCADE)
    numero_tessera = models.IntegerField()
    codice_fiscale = models.TextField()
    email = models.EmailField()
    data_iscrizione = models.DateField()
    quota_iscrizione = models.FloatField()
    scadenza_iscrizione = models.DateField()
    ultimo_rinnovo = models.DateField(auto_now_add=True)
    attivo = models.BooleanField(default=True)
    ruolo = models.ForeignKey(Consigliere, null=True, blank=True, on_delete=models.SET_NULL)
    consigliere_dal = models.DateField(null=True)
    data_creazione = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    objects = SociManager()

    class Meta:
        db_table = "soci"
        verbose_name = "Socio"
        verbose_name_plural = "Soci"


class EmailConsigliere(models.Model):
    email = models.EmailField()
    ruolo = models.ForeignKey(Consigliere, on_delete=models.CASCADE)
    socio = models.OneToOneField(Socio, null=True, blank=True, on_delete=models.DO_NOTHING)
    history = HistoricalRecords()

    class Meta:
        db_table = "email_consiglieri"
        verbose_name = "Email consigliere"
        verbose_name_plural = "Email consiglieri"


class RinnovoIscrizione(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.DO_NOTHING)
    data_rinnovo = models.DateField()
    quota_rinnovo = models.FloatField()
    history = HistoricalRecords()

    class Meta:
        db_table = "rinnovi"
        verbose_name = "Rinnovo iscrizione"
        verbose_name_plural = "Rinnovi iscrizioni"
