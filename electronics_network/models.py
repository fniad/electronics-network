from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings


class Manufacturer(models.Model):
    """ Производитель """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='владелец')
    name = models.CharField(max_length=255, verbose_name='название')
    email = models.EmailField(verbose_name='электронная почта')
    country = models.CharField(max_length=255, verbose_name='страна')
    city = models.CharField(max_length=255, verbose_name='город')
    street = models.CharField(max_length=255, verbose_name='улица')
    house_number = models.CharField(max_length=20, verbose_name='номер дома')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(0)], default=0,
                                verbose_name='уровень в иерархии')  # 0 для производителя

    def get_supplier(self):
        if self.level > 0:
            return self
        return None

    def __str__(self):
        return f"{self.name}"

    class Meta:
        """ Мета-данные """
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'


class RetailNetwork(models.Model):
    """ Розничная сеть """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='владелец')
    name = models.CharField(max_length=255, verbose_name='название')
    email = models.EmailField(verbose_name='электронная почта')
    country = models.CharField(max_length=255, verbose_name='страна')
    city = models.CharField(max_length=255, verbose_name='город')
    street = models.CharField(max_length=255, verbose_name='улица')
    house_number = models.CharField(max_length=20, verbose_name='номер дома')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.CASCADE,
                                     verbose_name='производитель')
    retail_network = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name='розничная сеть')
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)], default=1,
                                verbose_name='уровень в иерархии')  # 1 для розничной сети

    def clean(self):
        if self.level == 1 and self.manufacturer is None:
            raise ValidationError("У розничной сети должен быть производитель, у которого она закупается.")
        if self.level == 2 and self.retail_network is None:
            raise ValidationError("Добавьте поставщика из розничных сетей")
        if self.manufacturer and self.retail_network:
            raise ValidationError("Нельзя одновременно указывать производителя и розничную сеть.")


    def get_supplier(self):
        return self.manufacturer


    def __str__(self):
        return f"{self.name}"

    class Meta:
        """ Мета-данные """
        verbose_name = 'розничная сеть'
        verbose_name_plural = 'розничные сети'


class IndividualEntrepreneur(models.Model):
    """ Индивидуальный предприниматель """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='владелец')

    name = models.CharField(max_length=255, verbose_name='имя')
    email = models.EmailField(verbose_name='электронная почта')
    country = models.CharField(max_length=255, verbose_name='страна')
    city = models.CharField(max_length=255, verbose_name='город')
    street = models.CharField(max_length=255, verbose_name='улица')
    house_number = models.CharField(max_length=20, verbose_name='номер дома')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.CASCADE,
                                     verbose_name='производитель')
    retail_network = models.ForeignKey(RetailNetwork, null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name='розничная сеть')
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)],
                                verbose_name='уровень в иерархии')  # 2 для индивидуального предпринимателя

    def clean(self):
        if self.level == 1 and not self.manufacturer:
            raise ValidationError("Для первого уровня требуется закупаться у завода-производителя.")
        elif self.level == 2 and not self.retail_network:
            raise ValidationError("Для второго уровня требуется закупаться у сетевого поставщика.")

        if self.manufacturer and self.retail_network:
            raise ValidationError("Выберите только одного поставщика: завод или розничную сеть.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_supplier(self):
        if self.level == 1:
            return self.manufacturer
        elif self.level == 2:
            return self.retail_network
        else:
            return None

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'индивидуальный предприниматель'
        verbose_name_plural = 'индивидуальные предприниматели'


class Product(models.Model):
    """ Продукт """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='владелец')
    name = models.CharField(max_length=255, verbose_name='название')
    model = models.CharField(max_length=255, verbose_name='модель')
    release_date = models.DateField(verbose_name='дата выхода на рынок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.CASCADE,
                                     verbose_name='производитель')
    retailers = models.ManyToManyField(RetailNetwork, blank=True, verbose_name='розничные сети')
    entrepreneurs = models.ManyToManyField(IndividualEntrepreneur, blank=True, verbose_name='предприниматели')

    def get_supplier_levels(self):
        supplier_levels = []

        if self.manufacturer:
            supplier_levels.append(self.manufacturer.level)

        for retailer in self.retailers.all():
            supplier_levels.append(retailer.level)

        for entrepreneur in self.entrepreneurs.all():
            supplier_levels.append(entrepreneur.level)

        return supplier_levels

    def __str__(self):
        return f"{self.name} - {self.model}"

    class Meta:
        """ Мета-данные """
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Transaction(models.Model):
    """ Продажи """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='владелец')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='transactions', verbose_name='продукт')

    seller_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, blank=True,
                                            related_name='sales_manufacturer', verbose_name='продавец-производитель')
    seller_retail_network = models.ForeignKey(RetailNetwork, on_delete=models.CASCADE, null=True, blank=True,
                                              related_name='sales_retail_network',
                                              verbose_name='продавец-розничная сеть')
    seller_individual_entrepreneur = models.ForeignKey(IndividualEntrepreneur, on_delete=models.CASCADE,
                                                       null=True, blank=True,
                                                       related_name='sales_individual_entrepreneur',
                                                       verbose_name='продавец-индивидуальный предприниматель')

    buyer_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='purchases_manufacturer',
                                           verbose_name='покупатель-производитель')
    buyer_retail_network = models.ForeignKey(RetailNetwork, on_delete=models.CASCADE, null=True, blank=True,
                                             related_name='purchases_retail_network',
                                             verbose_name='покупатель-розничная сеть')
    buyer_individual_entrepreneur = models.ForeignKey(IndividualEntrepreneur, on_delete=models.CASCADE,
                                                      null=True, blank=True,
                                                      related_name='purchases_individual_entrepreneur',
                                                      verbose_name='покупатель-индивидуальный предприниматель')

    amount = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='количество')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='долг')

    def clean(self):
        seller_fields = [
            self.seller_manufacturer,
            self.seller_retail_network,
            self.seller_individual_entrepreneur,
        ]

        buyer_fields = [
            self.buyer_manufacturer,
            self.buyer_retail_network,
            self.buyer_individual_entrepreneur,
        ]

        if sum(bool(field) for field in seller_fields) != 1:
            raise ValidationError("Выберите только одно поле продавца.")

        if sum(bool(field) for field in buyer_fields) != 1:
            raise ValidationError("Выберите только одно поле покупателя.")

        product_suppliers = set()

        if self.product.manufacturer:
            product_suppliers.add(self.product.manufacturer)

        product_suppliers.update(self.product.retailers.all())
        product_suppliers.update(self.product.entrepreneurs.all())

        seller = next((field for field in seller_fields if field), None)

        if seller not in product_suppliers:
            raise ValidationError("Продавец не совпадает с поставщиком транзакции.")

    def __str__(self):
        return f"Продажа: {self.product.name} - Количество продукта: {self.amount} - Сумма долга: {self.debt}"

    class Meta:
        """ Мета-данные """
        verbose_name = 'транзакция'
        verbose_name_plural = 'транзакции'
