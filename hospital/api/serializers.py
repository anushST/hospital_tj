"""Serializers of the views."""
from rest_framework import serializers

from our_service.models import Category, Comment, Hospital, Rank, Service


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer."""

    class Meta:
        """Meta data of the CategorySerializer class."""

        model = Category
        fields = ('slug', 'title', 'description',)


class HospitalSerializer(serializers.ModelSerializer):
    """Hospital model serializer."""

    class Meta:
        """Meta data of the HospitalSerializer class."""

        model = Hospital
        fields = ('name', 'description', 'slug', 'category', 'work_time',
                  'average_rank', 'small_image', 'big_image', 'is_on_main',)


class ServiceSerializer(serializers.ModelSerializer):
    """Service model serializer."""

    class Meta:
        """Meta data of the ServiceSerializer class."""

        model = Service
        fields = ('id', 'name', 'description', 'category', 'price',
                  'min_price', 'max_price', 'hospital', 'average_rank',)


class CommentSerializer(serializers.ModelSerializer):
    """Comment model serializer."""

    class Meta:
        """Meta data of the CommentSerializer class."""

        model = Comment
        fields = ('id', 'text', 'author', 'created_at', 'updated_at',
                  'service', 'hospital',)
        read_only_fields = ('author', 'created_at', 'updated_at',
                            'service', 'hospital')


class RankSerializer(serializers.ModelSerializer):
    """Rank model serializer."""

    class Meta:
        """Meta data of the RankSerializer class."""

        model = Rank
        fields = ('id', 'value', 'author', 'created_at', 'updated_at',
                  'service', 'hospital',)
        read_only_fields = ('author', 'created_at', 'updated_at',
                            'service', 'hospital',)
