from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Consigliere, SezioneElsa, Socio, EmailConsigliere, RinnovoIscrizione

admin.site.register(Consigliere)
admin.site.register(SezioneElsa)
admin.site.register(Socio, SimpleHistoryAdmin)
admin.site.register(EmailConsigliere, SimpleHistoryAdmin)
admin.site.register(RinnovoIscrizione, SimpleHistoryAdmin)

# Register your models here.
