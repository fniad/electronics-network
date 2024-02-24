import django_filters
from rest_framework import viewsets, filters
from electronics_network.models import Manufacturer, RetailNetwork, IndividualEntrepreneur, Product, Transaction
from electronics_network.pagination import ManufacturerPagination, RetailNetworkPagination, \
    IndividualEntrepreneurPagination, ProductPagination, TransactionPagination
from electronics_network.permissions import IsOwnerOrSuperuser, IsActiveAuthenticatedUser
from electronics_network.serializers import ManufacturerSerializer, ProductSerializer, \
    IndividualEntrepreneurWriteSerializer, IndividualEntrepreneurReadSerializer, RetailNetworkWriteSerializer,\
    RetailNetworkReadSerializer, TransactionReadSerializer, TransactionWriteSerializer
from electronics_network.filters import ManufacturerFilter, ProductFilter


class ManufacturerViewSet(viewsets.ModelViewSet):
    """ Производитель """
    serializer_class = ManufacturerSerializer
    permission_classes = [IsOwnerOrSuperuser, IsActiveAuthenticatedUser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ManufacturerFilter
    search_fields = ['name', 'country']
    pagination_class = ManufacturerPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Manufacturer.objects.all().order_by('pk')
        else:
            return Manufacturer.objects.filter(owner=user).order_by('pk')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class RetailNetworkViewSet(viewsets.ModelViewSet):
    """ Розничная сеть """
    permission_classes = [IsOwnerOrSuperuser, IsActiveAuthenticatedUser]
    pagination_class = RetailNetworkPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RetailNetwork.objects.all().order_by('pk')
        else:
            return RetailNetwork.objects.filter(owner=user).order_by('pk')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RetailNetworkWriteSerializer
        else:
            return RetailNetworkReadSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class IndividualEntrepreneurViewSet(viewsets.ModelViewSet):
    """ Индивидуальный предприниматель """
    permission_classes = [IsOwnerOrSuperuser, IsActiveAuthenticatedUser]
    pagination_class = IndividualEntrepreneurPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return IndividualEntrepreneur.objects.all().order_by('pk')
        else:
            return IndividualEntrepreneur.objects.filter(owner=user).order_by('pk')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return IndividualEntrepreneurWriteSerializer
        else:
            return IndividualEntrepreneurReadSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    """ Продукт """
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrSuperuser, IsActiveAuthenticatedUser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'model']
    pagination_class = ProductPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Product.objects.all().order_by('pk')
        else:
            return Product.objects.filter(owner=user).order_by('pk')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    """ Продажи """
    permission_classes = [IsOwnerOrSuperuser, IsActiveAuthenticatedUser]
    pagination_class = TransactionPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Transaction.objects.all().order_by('pk')
        else:
            return Transaction.objects.filter(owner=user).order_by('pk')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TransactionReadSerializer
        return TransactionWriteSerializer


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
