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

class RetailNetworkWriteSerializer(serializers.ModelSerializer):
    """ Розничная сеть для записи """

    class Meta:
        model = RetailNetwork
        fields = '__all__'
        extra_kwargs = {
            'manufacturer': {'required': False},
            'retail_network': {'required': False},
        }

    def validate(self, data):
        level = data.get('level')
        manufacturer = data.get('manufacturer')
        retail_network = data.get('retail_network')

        if level == 1 and not manufacturer:
            raise serializers.ValidationError("Для первого уровня требуется закупаться у завода-производителя.")
        elif level == 2 and not retail_network:
            raise serializers.ValidationError("Для второго уровня требуется закупаться у сетевого поставщика.")

        if manufacturer and retail_network:
            raise serializers.ValidationError("Выберите только одного поставщика: завод или розничную сеть.")

        return data


class RetailNetworkReadSerializer(serializers.ModelSerializer):
    """ Розничная сеть для чтения """

    retail_network = RetailNetworkOnlyNameSerializer(read_only=True)
    manufacturer = ManufacturerOnlyNameSerializer(read_only=True)

    class Meta:
        model = RetailNetwork
        fields = '__all__'


class IndividualEntrepreneurWriteSerializer(serializers.ModelSerializer):
    """ Индивидуальный предприниматель для записи """

    class Meta:
        model = IndividualEntrepreneur
        fields = '__all__'
        extra_kwargs = {
            'manufacturer': {'required': False},
            'retail_network': {'required': False},
        }

    def validate(self, data):
        level = data.get('level')
        manufacturer = data.get('manufacturer')
        retail_network = data.get('retail_network')

        if level == 1 and not manufacturer:
            raise serializers.ValidationError("Для первого уровня требуется закупаться у завода-производителя.")
        elif level == 2 and not retail_network:
            raise serializers.ValidationError("Для второго уровня требуется закупаться у сетевого поставщика.")

        if manufacturer and retail_network:
            raise serializers.ValidationError("Выберите только одного поставщика: завод или розничную сеть.")

        return data


class IndividualEntrepreneurReadSerializer(serializers.ModelSerializer):
    """ Индивидуальный предприниматель для чтения """

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