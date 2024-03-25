"""Register our_service models in admin_zone here."""
from django.contrib import admin

from .models import Comment, Hospital, Rank, Service

admin.site.register([Comment, Hospital, Rank, Service])
