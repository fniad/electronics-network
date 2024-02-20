from rest_framework import serializers
from electronics_network.models import Manufacturer, RetailNetwork, IndividualEntrepreneur, Product, Transaction


class ManufacturerOnlyNameSerializer(serializers.ModelSerializer):
    """ Производитель наименование """
    class Meta:
        model = Manufacturer
        fields = ['name']


class RetailNetworkOnlyNameSerializer(serializers.ModelSerializer):
    """ Розничная сеть наименование """
    class Meta:
        model = RetailNetwork
        fields = ['name']


class IndividualEntrepreneurOnlyNameSerializer(serializers.ModelSerializer):
    """ Индивидуальный предприниматель наименование """
    class Meta:
        model = IndividualEntrepreneur
        fields = ['name']


class ManufacturerSerializer(serializers.ModelSerializer):
    """ Производитель """

    class Meta:
        model = Manufacturer
        fields = '__all__'


class RetailNetworkSerializer(serializers.ModelSerializer):
    """ Розничная сеть """

    retail_network = RetailNetworkOnlyNameSerializer(read_only=True)
    manufacturer = ManufacturerOnlyNameSerializer(read_only=True)

    class Meta:
        model = RetailNetwork
        fields = '__all__'


class IndividualEntrepreneurSerializer(serializers.ModelSerializer):
    """ Индивидуальный предприниматель """

    retail_network = RetailNetworkOnlyNameSerializer(read_only=True)
    manufacturer = ManufacturerOnlyNameSerializer(read_only=True)

    class Meta:
        model = IndividualEntrepreneur
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """ Продукт """
    retailers = RetailNetworkOnlyNameSerializer(many=True, read_only=True)
    entrepreneurs = IndividualEntrepreneurOnlyNameSerializer(many=True, read_only=True)
    manufacturer = ManufacturerOnlyNameSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date', 'created_at', 'owner', 'manufacturer', 'retailers', 'entrepreneurs']


class TransactionSerializer(serializers.ModelSerializer):
    """ Продажи """
    product = serializers.StringRelatedField()
    seller_manufacturer = serializers.StringRelatedField()
    seller_retail_network = serializers.StringRelatedField()
    seller_individual_entrepreneur = serializers.StringRelatedField()
    buyer_manufacturer = serializers.StringRelatedField()
    buyer_retail_network = serializers.StringRelatedField()
    buyer_individual_entrepreneur = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = '__all__'