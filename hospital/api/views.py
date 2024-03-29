"""Views of the api."""
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError

from .filters import PriceFilter
from .permissions import OwnerOrReadOnly
from .serializers import (
    CategorySerializer, CommentSerializer, HospitalSerializer,
    RankSerializer, ServiceSerializer)
from our_service.models import Category, Hospital, Rank, Service


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Category viewset."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('title',)
    lookup_field = 'slug'


class HospitalServiceBaseViewSet(viewsets.ReadOnlyModelViewSet):
    """Hospital and Service base viewset."""

    def get_queryset(self):
        """Get queryset for viewset.

        Ovverided to check param 'category'
        """
        queryset = super().get_queryset()
        if self.action == 'list':
            category_slug = self.request.query_params.get('category')
            return (queryset.filter(category__slug=category_slug)
                    if category_slug is not None else queryset)
        return queryset


class HospitalViewSet(HospitalServiceBaseViewSet):
    """Hospital viewset."""

    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ServiceViewSet(HospitalServiceBaseViewSet):
    """Service viewset."""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = (SearchFilter, PriceFilter)
    search_fields = ('name',)


class CommentRankBaseViewSet(viewsets.ModelViewSet):
    """Base ViewSet for Comment and Rank viewsets."""

    filter_backends = (OrderingFilter,)
    ordering_fields = ('updated_at',)
    permission_classes = (OwnerOrReadOnly,)

    def get_hospital(self) -> Hospital:
        """Get hospital object."""
        return get_object_or_404(Hospital, slug=self.kwargs['hospital_slug'])

    def get_service(self) -> Service:
        """Get service object."""
        return get_object_or_404(Service, pk=self.kwargs['service_id'])

    def perform_create(self, serializer: ModelSerializer) -> None:
        """Save serializer."""
        path = self.request.get_full_path()
        if '/services/' in path:
            serializer.save(author=self.request.user,
                            service=self.get_service())
        elif '/hospitals/' in path:
            serializer.save(author=self.request.user,
                            hospital=self.get_hospital())


class CommentViewSet(CommentRankBaseViewSet):
    """Comment viewset."""

    serializer_class = CommentSerializer

    def get_queryset(self) -> QuerySet:
        """Get queryset for viewset."""
        path = self.request.get_full_path()
        if '/services/' in path:
            return self.get_service().service_comment.all()
        if '/hospitals/' in path:
            return self.get_hospital().hospital_comment.all()


class RankViewSet(CommentRankBaseViewSet):
    """Rank viewset."""

    serializer_class = RankSerializer

    def get_queryset(self) -> QuerySet:
        """Get queryset for viewset."""
        path = self.request.get_full_path()
        if '/services/' in path:
            return self.get_service().service_rank.all()
        if '/hospitals/' in path:
            return self.get_hospital().hospital_rank.all()

    def perform_create(self, serializer: ModelSerializer) -> None:
        """Save serializer."""
        path = self.request.get_full_path()
        # Start Validation
        try:
            if '/services/' in path:
                Rank.objects.get(
                    author=self.request.user, service=self.get_service())
            if '/hospitals/' in path:
                Rank.objects.get(
                    author=self.request.user, hospital=self.get_hospital())
            raise ValidationError('You already ranked.')
        except ObjectDoesNotExist:
            pass
        # End Validation
        return super().perform_create(serializer)
