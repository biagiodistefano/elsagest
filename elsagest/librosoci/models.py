from django.db import models

# Create your models here.


class SezioneElsa(models.Model):
    citta = models.TextField()

    class Meta:
        db_table = "sezioni_elsa"


class Socio(models.Model):
    nome = models.TextField()
    cognome = models.TextField()
    sezione = models.ForeignKey(SezioneElsa, on_delete=models.DO_NOTHING)
    data_di_nascita = models.DateField()
    codice_fiscale = models.TextField()
    email = models.EmailField()
    data_iscrizione = models.DateField()
    scadenza_iscrizione = models.DateField()
    attivo = models.BooleanField(default=True)

    class Meta:
        db_table = "soci"


class RinnovoIscrizione(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.DO_NOTHING)
    data_rinnovo = models.DateField()
    quota_rinnovo = models.FloatField()

    class Meta:
        db_table = "rinnovi"
