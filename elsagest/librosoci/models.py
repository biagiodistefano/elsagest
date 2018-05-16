from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class SezioneElsa(models.Model):
    nome = models.TextField()
    users = models.ManyToManyField(User)

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


class Socio(models.Model):
    nome = models.TextField()
    cognome = models.TextField()
    sezione = models.ForeignKey(SezioneElsa, on_delete=models.CASCADE)
    numero_tessera = models.IntegerField()
    codice_fiscale = models.TextField()
    email = models.EmailField()
    data_iscrizione = models.DateField()
    scadenza_iscrizione = models.DateField()
    ultimo_rinnovo = models.DateField(auto_now_add=True)
    attivo = models.BooleanField(default=True)
    ruolo = models.ForeignKey(Consigliere, on_delete=models.DO_NOTHING)
    consigliere_dal = models.DateField(null=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "soci"
        verbose_name = "Socio"
        verbose_name_plural = "Soci"


class EmailConsigliere(models.Model):
    email = models.EmailField()
    ruolo = models.ForeignKey(Consigliere, on_delete=models.CASCADE)
    socio = models.OneToOneField(Socio, null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "email_consiglieri"
        verbose_name = "Email consigliere"
        verbose_name_plural = "Email consiglieri"


class RinnovoIscrizione(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.DO_NOTHING)
    data_rinnovo = models.DateField()
    quota_rinnovo = models.FloatField()

    class Meta:
        db_table = "rinnovi"
        verbose_name = "Rinnovo iscrizione"
        verbose_name_plural = "Rinnovi iscrizioni"


class ModificheRinnovoSoci(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.DO_NOTHING)
    data_rinnovo = models.DateField()
    quota_rinnovo = models.FloatField()
    rinnovo_iscrizione = models.ForeignKey(RinnovoIscrizione, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "modifiche_rinnovi"
        verbose_name = "Modifica rinnovo iscrizione"
        verbose_name_plural = "Modifiche rinnovi iscrizioni"


class ModificheSoci(models.Model):
    nome = models.TextField()
    cognome = models.TextField()
    sezione = models.ForeignKey(SezioneElsa, on_delete=models.DO_NOTHING)
    data_di_nascita = models.DateField()
    codice_fiscale = models.TextField()
    email = models.EmailField()
    data_iscrizione = models.DateField()
    scadenza_iscrizione = models.DateField()
    attivo = models.BooleanField(default=True)
    ruolo = models.ForeignKey(Consigliere, on_delete=models.DO_NOTHING)
    data_creazione = models.DateTimeField()
    dati_dal = models.DateTimeField()
    dati_al = models.DateTimeField(auto_now_add=True)
    socio = models.ForeignKey(Socio, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "modifiche_soci"
        verbose_name = "Modifica socio"
        verbose_name_plural = "Modifiche soci"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sezione = models.ForeignKey(SezioneElsa, on_delete=models.CASCADE, default=1)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
