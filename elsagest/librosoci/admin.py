from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Ruolo, SezioneElsa, Socio, EmailConsigliere, RinnovoIscrizione

admin.site.register(Ruolo)
admin.site.register(SezioneElsa)
admin.site.register(Socio, SimpleHistoryAdmin)
admin.site.register(EmailConsigliere, SimpleHistoryAdmin)
admin.site.register(RinnovoIscrizione, SimpleHistoryAdmin)

# Register your models here.
