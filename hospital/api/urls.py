"""URLs for api app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .constants import API_VERSION

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('hospitals', views.HospitalViewSet, basename='hospital')
router.register('services', views.ServiceViewSet, basename='service')
router.register(r'^hospitals/(?P<hospital_slug>[-\w]+)/comments',
                views.CommentViewSet, basename='hospital_comment')
router.register(r'^services/(?P<service_id>\d+)/comments',
                views.CommentViewSet, basename='service_comment')
router.register(r'^hospitals/(?P<hospital_slug>[-\w]+)/ranks',
                views.RankViewSet, basename='hospital_rank')
router.register(r'^services/(?P<service_id>\d+)/ranks',
                views.RankViewSet, basename='service_rank')

urlpatterns = [
    path(f'{API_VERSION}/', include('users.urls')),
    path(f'{API_VERSION}/', include(router.urls)),
]
