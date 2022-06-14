from django.contrib import admin
from .models import Url


#register my models in SQLite Database

class UrlAdmin(admin.ModelAdmin):
    list_display = ('pk', 'short_url', 'full_url', 'redirects')

admin.site.register(Url, UrlAdmin)

