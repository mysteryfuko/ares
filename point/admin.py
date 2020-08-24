from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import epgp,DKPtable,status

admin.site.register(epgp)
admin.site.register(DKPtable)
admin.site.register(status)
