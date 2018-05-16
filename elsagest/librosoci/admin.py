from django.contrib import admin
from .models import Consigliere, SezioneElsa, Socio, EmailConsigliere, RinnovoIscrizione, ModificheSoci, UserProfile

admin.site.register(Consigliere)
admin.site.register(SezioneElsa)
admin.site.register(Socio)
admin.site.register(EmailConsigliere)
admin.site.register(RinnovoIscrizione)
admin.site.register(ModificheSoci)
admin.site.register(UserProfile)

# Register your models here.
