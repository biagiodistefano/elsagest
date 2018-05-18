from django.db import models
from django.contrib.auth.models import User
from librosoci.models import Socio
# Create your models here.


class Email(models.Model):
    oggetto = models.TextField()
    corpo = models.TextField()
    mittente = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="sender")
    destinatari = models.ManyToManyField(Socio, related_name="email_destinatari")
    inviata_il = models.DateTimeField(auto_now_add=True)
