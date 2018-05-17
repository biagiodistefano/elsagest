from django.contrib import admin
from .models import UserProfile
from simple_history.admin import SimpleHistoryAdmin


admin.site.register(UserProfile, SimpleHistoryAdmin)

# Register your models here.
