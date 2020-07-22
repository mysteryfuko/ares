from django.contrib import admin

# Register your models here.
from .models import score,record,user,xiaohao

admin.site.register(score)
admin.site.register(record)
admin.site.register(user)
admin.site.register(xiaohao)