from django.contrib import admin
from .models import Document,User

# Register your models here.
admin.site.register([Document,User])
