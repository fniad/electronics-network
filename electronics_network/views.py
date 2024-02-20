import django_filters
from rest_framework import viewsets, filters
from electronics_network.models import Manufacturer, RetailNetwork, IndividualEntrepreneur, Product, Transaction
from electronics_network.permissions import IsOwnerOrSuperuser
from electronics_network.serializers import ManufacturerSerializer, RetailNetworkSerializer, \
    IndividualEntrepreneurSerializer, ProductSerializer, TransactionSerializer
from electronics_network.filters import ManufacturerFilter, ProductFilter


class ManufacturerViewSet(viewsets.ModelViewSet):
    """ Производитель """
    serializer_class = ManufacturerSerializer
    permission_classes = [IsOwnerOrSuperuser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ManufacturerFilter
    search_fields = ['name', 'country']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Manufacturer.objects.all()
        else:
            return Manufacturer.objects.filter(owner=user)


class RetailNetworkViewSet(viewsets.ModelViewSet):
    """ Розничная сеть """
    serializer_class = RetailNetworkSerializer
    permission_classes = [IsOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RetailNetwork.objects.all()
        else:
            return RetailNetwork.objects.filter(owner=user)


class IndividualEntrepreneurViewSet(viewsets.ModelViewSet):
    """ Индивидуальный предприниматель """
    serializer_class = IndividualEntrepreneurSerializer
    permission_classes = [IsOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return IndividualEntrepreneur.objects.all()
        else:
            return IndividualEntrepreneur.objects.filter(owner=user)


class ProductViewSet(viewsets.ModelViewSet):
    """ Продукт """
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrSuperuser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'model']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Product.objects.all()
        else:
            return Product.objects.filter(owner=user)


class TransactionViewSet(viewsets.ModelViewSet):
    """ Продажи """
    serializer_class = TransactionSerializer
    permission_classes = [IsOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Transaction.objects.all()
        else:
            return Transaction.objects.filter(owner=user)
