"""URLs for api app."""
from django.urls import include, path

from .constants import API_VERSION

urlpatterns = [
    path(f'{API_VERSION}/', include('users.urls')),
]
