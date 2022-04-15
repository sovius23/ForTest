from django_filters.rest_framework import FilterSet, RangeFilter, CharFilter
from api.models import Article


class Filters(FilterSet):
    title = CharFilter()

    class Meta:
        model = Article
        fields = ["title", ]
