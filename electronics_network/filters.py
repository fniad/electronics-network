import django_filters
from electronics_network.models import Manufacturer, Product


class ManufacturerFilter(django_filters.FilterSet):
    """ Фильтр производителя """
    country = django_filters.CharFilter(field_name='country', lookup_expr='iexact')

    class Meta:
        model = Manufacturer
        fields = ['country']

class ProductFilter(django_filters.FilterSet):
    """ Фильтр продукта """
    country = django_filters.CharFilter(field_name='manufacturer__country', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['country']