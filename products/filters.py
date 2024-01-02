import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    # the word that i search for in name will be case insensitive & can be a part of the word
    name = django_filters.CharFilter(lookup_expr='icontains')
    # the word that i search for in category will be case insensitive & should match the exact word
    category = django_filters.CharFilter(field_name='category' ,lookup_expr='iexact')
    # min & max price will be used to filter the products based on range of prices
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'min_price', 'max_price', 'ratings', 'name']