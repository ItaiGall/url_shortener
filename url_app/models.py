from django.db import models

#At the beginning I tried to connect a separate model for a full_url
#via a foreign key, but ultimately I kept only one model for simplicity
class Url(models.Model):
    # satisfy the requirement for a unique short url, mapping to any full url, including existing ones
    #URLField validates the correct URL format
    full_url = models.URLField(max_length=300)
    #I recconed whether to to define "short_url" as a unique field
    #but before saving a generated short url in views "create" method, I do a duplicate check
    short_url = models.CharField(editable=False, unique=True, blank=None, max_length=15)
    #No. of clicks
    redirects = models.IntegerField(default=0, blank=False, editable=False)