"""Register our_service models in admin_zone here."""
from django.contrib import admin

from .models import Category, Comment, Hospital, Rank, Service

admin.site.register([Category, Comment, Hospital, Rank, Service])
