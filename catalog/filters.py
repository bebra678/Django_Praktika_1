import django_filters
from .models import Design


class CategoryFilters(django_filters.FilterSet):
    class Meta:
        model = Design
        exclude = ['image']
        fields = ['category']
