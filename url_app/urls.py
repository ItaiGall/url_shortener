from django.urls import path
from .views import UrlViewSet

urlpatterns = [
    #GET the complete list
    path('', UrlViewSet.as_view({
        'get': 'list',
    })),
    #POST a new entry
    path('create', UrlViewSet.as_view({
        'post': 'create',
    })),
    #query entry by id, update entry or delete it
    path('<str:pk>', UrlViewSet.as_view({
        'get': 'list',
        'put': 'update',
        'delete': 'destroy',
    })),
    #'retrieve' method ultimately redirects to full length url
    #update or delete entry by short_url.
    #id, short_url and clicks are non editable parameters
    path('s/<str:short_url>', UrlViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
]