from django.db import models
from django.contrib.auth.models import User
from librosoci.models import SezioneElsa
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from fernet_fields import EncryptedTextField

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sezione = models.ForeignKey(SezioneElsa, on_delete=models.CASCADE, default=1)
    history = HistoricalRecords()

    def __str__(self):
        return f"Profilo di {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class EmailCredentials(models.Model):

    username = models.EmailField()
    password = EncryptedTextField() # will be encrypted... but... BIG security issue!
    host = models.TextField()
    port = models.IntegerField()
    tls = models.BooleanField()
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

