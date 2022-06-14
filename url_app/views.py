from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from .models import Url
from .serializers import UrlSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .url_shortener import shorten_url
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
import threading

class UrlViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer

    def __init__(self):
        self.lock = threading.Lock()
    #override the create method to inject the url_shortener algorithm
    #URL: api/create
    def create(self, request, *args, **kwargs):
        serializer = UrlSerializer(data=request.data)
        full_exist_url = serializer.initial_data["full_url"]
        #if full_url already in db, return existing short_url
        #lock thread to prevent TOCTOU
        self.lock.acquire()
        try:
            existing_entry = Url.objects.get(full_url=full_exist_url)
            serializer_exist = UrlSerializer(existing_entry, many=False)
            return Response(serializer_exist.data, status=status.HTTP_208_ALREADY_REPORTED)
        except ObjectDoesNotExist:
            #create a shortened temporary url and confirm that it is no duplicate
            #while True:
            tempshort = shorten_url()
            #    if not Url.objects.filter(short_url=tempshort):
            #        break
            #add unique shortened url to created object
            if serializer.is_valid(raise_exception=True):
                serializer.save(short_url=tempshort)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        finally:
            self.lock.release()

    #override retrieve method to call a short_url, redirect it to the full_url
    #and finally increment the "redirects" counter, if redirect was successful
    # URL: api/s/<str:short_url>
    def retrieve(self, request, short_url=None):
        #get the right record according to requested short_url or return 404
        record = get_object_or_404(Url, short_url=short_url)
        #increment redirects value
        record.redirects = F('redirects') + 1
        record.save()
        #redirect to full_url in record
        return HttpResponseRedirect(record.full_url)