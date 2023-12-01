from django.contrib import admin
from . import models

admin.site.register(models.Contact)
admin.site.register(models.User)
admin.site.register(models.Signature)
admin.site.register(models.OtpCode)
admin.site.register(models.PasswordHistory)
