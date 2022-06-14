from .models import Url
from rest_framework import serializers

class UrlSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(max_length=15, read_only=True)
    redirects = serializers.IntegerField(read_only=True)

    class Meta:
        model = Url
        fields = ['id', 'full_url', 'short_url', 'redirects']