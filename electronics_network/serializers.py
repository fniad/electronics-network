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


class TransactionReadSerializer(serializers.ModelSerializer):
    """ Транзакция для чтения """
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


class TransactionWriteSerializer(serializers.ModelSerializer):
    """ Транзакция для записи """
    class Meta:
        model = Transaction
        fields = '__all__'
        extra_kwargs = {
            'product': {'required': True},
            'seller_manufacturer': {'required': True},
            'seller_retail_network': {'required': True},
            'seller_individual_entrepreneur': {'required': True},
            'buyer_manufacturer': {'required': True},
            'buyer_retail_network': {'required': True},
            'buyer_individual_entrepreneur': {'required': True},
        }

    def validate(self, data):
        seller_fields = [
            data['seller_manufacturer'],
            data['seller_retail_network'],
            data['seller_individual_entrepreneur'],
        ]

        buyer_fields = [
            data['buyer_manufacturer'],
            data['buyer_retail_network'],
            data['buyer_individual_entrepreneur'],
        ]

        if sum(bool(field) for field in seller_fields) != 1:
            raise serializers.ValidationError("Выберите только одно поле продавца.")

        if sum(bool(field) for field in buyer_fields) != 1:
            raise serializers.ValidationError("Выберите только одно поле покупателя.")

        product_suppliers = set()

        if data['product'].manufacturer:
            product_suppliers.add(data['product'].manufacturer)

        product_suppliers.update(data['product'].retailers.all())
        product_suppliers.update(data['product'].entrepreneurs.all())

        seller = next((field for field in seller_fields if field), None)

        if seller not in product_suppliers:
            raise serializers.ValidationError("Продавец не совпадает с поставщиком транзакции.")

        return data