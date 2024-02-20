from django.contrib import admin
from .models import Manufacturer, RetailNetwork, IndividualEntrepreneur, Product, Transaction


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """ Производитель """
    list_display = ('name', 'email', 'country', 'city', 'get_supplier')
    search_fields = ('name', 'city')
    list_filter = ('city', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(manufacturer_user=request.user)
        return qs

@admin.register(RetailNetwork)
class RetailNetworkAdmin(admin.ModelAdmin):
    """ Розничная сеть """
    list_display = ('name', 'email', 'country', 'city', 'get_supplier')
    search_fields = ('name', 'city')
    list_filter = ('city', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(retailers_user=request.user)
        return qs


@admin.register(IndividualEntrepreneur)
class IndividualEntrepreneurAdmin(admin.ModelAdmin):
    """ Индивидуальный предприниматель """
    list_display = ('name', 'email', 'country', 'city', 'get_supplier')
    search_fields = ('name', 'city')
    list_filter = ('city', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(entrepreneurs_user=request.user)
        return qs


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Продукт """
    list_display = ('name', 'model', 'release_date', 'get_supplier_levels', 'created_at')
    search_fields = ('name', 'model')
    list_filter = ('release_date', )

    def get_supplier_levels(self, obj):
        return ', '.join(map(str, obj.get_supplier_levels()))

    get_supplier_levels.short_description = 'Уровни поставщиков'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Если пользователь не является суперпользователем, фильтруем только его собственные продукты
        if not request.user.is_superuser:
            qs = qs.filter(manufacturer_user=request.user) | qs.filter(retailers_user=request.user) | qs.filter(
                entrepreneurs_user=request.user)
        return qs


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """ Транзакция """
    list_display = ('product', 'get_seller', 'get_buyer', 'amount', 'debt', 'get_created_at')
    search_fields = ('product__name', 'seller_manufacturer__name', 'buyer_manufacturer__name')
    list_filter = ('product__created_at', 'seller_manufacturer', 'seller_retail_network',
                   'seller_individual_entrepreneur', 'buyer_manufacturer', 'buyer_retail_network',
                   'buyer_individual_entrepreneur')

    def get_seller(self, obj):
        seller_manufacturer = getattr(obj, 'seller_manufacturer', None)
        seller_retail_network = getattr(obj, 'seller_retail_network', None)
        seller_individual_entrepreneur = getattr(obj, 'seller_individual_entrepreneur', None)

        if seller_manufacturer:
            return str(seller_manufacturer)
        elif seller_retail_network:
            return str(seller_retail_network)
        elif seller_individual_entrepreneur:
            return str(seller_individual_entrepreneur)
        else:
            return "Unknown Seller"

    def get_buyer(self, obj):
        buyer_manufacturer = getattr(obj, 'buyer_manufacturer', None)
        buyer_retail_network = getattr(obj, 'buyer_retail_network', None)
        buyer_individual_entrepreneur = getattr(obj, 'buyer_individual_entrepreneur', None)

        if buyer_manufacturer:
            return str(buyer_manufacturer)
        elif buyer_retail_network:
            return str(buyer_retail_network)
        elif buyer_individual_entrepreneur:
            return str(buyer_individual_entrepreneur)
        else:
            return "Unknown Buyer"

    def get_created_at(self, obj):
        return obj.product.created_at

    get_seller.short_description = 'Продавец'
    get_buyer.short_description = 'Покупатель'
    get_created_at.short_description = 'Дата создания'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Если пользователь не является суперпользователем, фильтруем только его собственные транзакции
        if not request.user.is_superuser:
            qs = qs.filter(seller_user=request.user) | qs.filter(buyer_user=request.user)
        return qs
