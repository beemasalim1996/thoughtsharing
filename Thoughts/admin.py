from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CustUser)
admin.site.register(models.Thoughts)