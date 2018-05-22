from django.db import models
from django.contrib.auth.models import User
from librosoci.models import Socio
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class Email(models.Model):
    oggetto = models.TextField()
    corpo = models.TextField()
    mittente = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="sender")
    inviata_il = models.DateTimeField(auto_now_add=True)
    # destinatari = Prima o poi lo implemento

class BozzaEmail(models.Model):
    oggetto = models.TextField()
    corpo = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creata_il = models.DateTimeField(auto_now_add=True)
    disponibile_per = models.IntegerField()  # 0: privata; 1: sezione di appartenenza; 2: tutti


class UnsubscribeToken(models.Model):
    socio = models.OneToOneField(Socio, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4(), editable=False)


@receiver(post_save, sender=Socio)
def create_unsubscribe_token(sender, instance, created, **kwargs):
    if created:
        print('ok')
        UnsubscribeToken.objects.create(socio=instance)


@receiver(post_save, sender=Socio)
def save_unsubscribe_token(sender, instance, **kwargs):
    instance.unsubscribetoken.save()
