import django_filters
from .models import *

class FilterPro(django_filters.FilterSet):
    price=django_filters.NumberFilter()
    categories=django_filters.CharFilter(lookup_expr='icontains')
    brand=django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        modedl=items
        fields='__all__'

