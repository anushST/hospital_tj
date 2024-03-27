"""Filters of the api."""
from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class PriceFilter(BaseFilterBackend):
    """The filter for price.

    URL_params (note: they can't be used seperately):
        min_price: min price of filter (note: can't be less than 1)
        max_price: max price of the filter
    """

    def filter_queryset(self, request, queryset, view):
        """Return filtered queryset."""
        min_price: str | None = request.query_params.get('min_price')
        max_price: str | None = request.query_params.get('max_price')

        if min_price is not None and max_price is not None:
            min_price = int(min_price)
            max_price = int(max_price)
            if min_price < 1 or max_price < min_price:
                return queryset
            return queryset.filter(
                (~Q(price=0) & Q(price__gte=min_price)
                    & Q(price__lte=max_price)) |
                (~Q(max_price=0) & Q(max_price__gte=min_price)
                    & Q(max_price__lte=max_price))
            )
        return queryset
