from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from datetime import date, timedelta
from django.utils import timezone


# Create your models here.


class SezioneElsa(models.Model):
    nome = models.TextField()
    history = HistoricalRecords()

    class Meta:
        db_table = "sezioni_elsa"
        verbose_name = "Sezione ELSA"
        verbose_name_plural = "Sezioni ELSA"

    def __str__(self):
        return f"ELSA {self.nome}"


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
    data_creazione = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    objects = SociManager()

    @property
    def scaduto(self):
        return self.scadenza_iscrizione < date.today()

    @property
    def promemoria_inviato(self):
        return Reminder.objects.filter(destinatari=self) and Reminder.objects.filter(destinatari=self).last().recent

    @property
    def iscritto_il(self):
        return self.data_iscrizione.strftime("%d-%m-%Y")

    @property
    def scade_il(self):
        return self.scadenza_iscrizione.strftime("%d-%m-%Y")

    @property
    def rinnovato_il(self):
        return self.ultimo_rinnovo.strftime("%d-%m-%Y")

    @property
    def nome_esteso(self):
        return f"{self.nome} {self.cognome}"

    class Meta:
        db_table = "soci"
        verbose_name = "Socio"
        verbose_name_plural = "Soci"


class Ruolo(models.Model):
    ruolo = models.TextField()
    soci = models.ManyToManyField(Socio, through="RuoliSoci", related_name="ruolo_socio")

    class Meta:
        db_table = "ruoli_consiglieri"
        verbose_name = "Consigliere"
        verbose_name_plural = "Consiglieri"


class RuoliSoci(models.Model):
    ruolo = models.ForeignKey(Ruolo, on_delete=models.CASCADE)
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    consigliere_dal = models.DateField(auto_now_add=True)

    @property
    def in_carica_dal(self):
        return self.consigliere_dal.strftime("%d-%m-%Y")


class EmailConsigliere(models.Model):
    email = models.EmailField()
    ruolo = models.ForeignKey(Ruolo, on_delete=models.CASCADE)
    socio = models.OneToOneField(Socio, on_delete=models.CASCADE)
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


class ReminderManager(models.Manager):

    def last(self):
        return self.get_queryset().orderby('-inviata_il')


class Reminder(models.Model):
    mittente = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="reminder")
    destinatari = models.ManyToManyField(Socio, related_name="remaindee")
    inviata_il = models.DateTimeField(auto_now_add=True)

    @property
    def recent(self):
        return (timezone.now() - self.inviata_il).days < 15

    @property
    def not_recent(self):
        return (timezone.now() - self.inviata_il).days > 15
