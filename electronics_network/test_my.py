""" Тесты для authorization_service """
import json

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from electronics_network.models import Manufacturer, RetailNetwork, IndividualEntrepreneur, Product, Transaction
from users.models import User


@pytest.fixture
def user_first():
    """ Кэшируемая фикстура для создания первого пользователя """
    return User.objects.create_user(
        username='test_active',
        password='test',
        is_active=True
    )


@pytest.fixture
def user_second():
    """ Фикстура для создания второго пользователя """
    return User.objects.create_user(
        username='admin',
        password='admin',
        is_active=True,
        is_superuser=True
    )


@pytest.fixture
def api_client():
    """ Фикстура для создания API клиента """
    return APIClient()


@pytest.fixture
def jwt_token_for_first_user(user_first):
    """ Фикстура для создания JWT токена """
    token = AccessToken.for_user(user_first)
    return f'Bearer {token}'


@pytest.fixture
def jwt_token_for_second_user(user_second):
    """ Фикстура для создания JWT токена """
    token = AccessToken.for_user(user_second)
    return f'Bearer {token}'


@pytest.fixture
def first_manufacturer(user_first):
    return Manufacturer.objects.create(
        name="Гамма",
        email="gamma@yandex.ru",
        country="Россия",
        city="Санкт-Петербург",
        street="Римского-Корсакова",
        house_number="54",
        level=0,
        owner=user_first
    )


@pytest.fixture
def first_retail_network(user_first, first_manufacturer):
    return RetailNetwork.objects.create(
        manufacturer=first_manufacturer,
        retail_network=None,
        name="Серебро",
        email="serebro@yandex.ru",
        country="Россия",
        city="Санкт-Петербург",
        street="ул Кржижановского",
        house_number="54",
        level=1,
        owner=user_first
    )


@pytest.fixture
def second_retail_network(user_first, first_retail_network):
    return RetailNetwork.objects.create(
        manufacturer=None,
        retail_network=first_retail_network,
        name="Золото",
        email="gold@yandex.ru",
        country="Россия",
        city="Санкт-Петербург",
        street="ул Кржижановского",
        house_number="22",
        level=2,
        owner=user_first
    )


@pytest.fixture
def first_individual_entrepreneur(user_first, first_manufacturer):
    return IndividualEntrepreneur.objects.create(
        name="Крис Кэтт",
        email="criscat@gmail.com",
        country="Россия",
        city="Санкт-Петербург",
        street="ул Чайковского",
        house_number="7",
        level=1,
        manufacturer=first_manufacturer,
        retail_network=None,
        owner=user_first
    )


@pytest.fixture
def first_product(user_first, first_manufacturer):
    return Product.objects.create(
        name="Тестовая продукция",
        model="Тест",
        release_date="2024-02-20",
        created_at="2024-02-20T15:32:03.268284+03:00",
        owner=user_first,
        manufacturer=first_manufacturer,
    )


@pytest.fixture
def first_transaction(user_first, first_product, first_manufacturer, first_retail_network):
    return Transaction.objects.create(
        product=first_product,
        seller_manufacturer=first_manufacturer,
        seller_retail_network=None,
        seller_individual_entrepreneur=None,
        buyer_manufacturer=None,
        buyer_retail_network=first_retail_network,
        buyer_individual_entrepreneur=None,
        amount=10,
        debt="10000.00",
        owner=user_first
    )


# Тесты для работы с заводами


@pytest.mark.django_db
def test_get_list_manufacturer_api(api_client, user_first, jwt_token_for_first_user):
    """ Тест для получения списка производителей """
    api_client.force_authenticate(user=user_first)
    response = api_client.get('/manufacturers/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_detail_manufacturer_api(api_client, user_first, jwt_token_for_first_user, first_manufacturer):
    """ Тест для получения деталей производителя """
    api_client.force_authenticate(user=user_first)
    response = api_client.get(f'/manufacturers/{first_manufacturer.id}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_manufacturer_api(api_client, user_first, jwt_token_for_first_user):
    """ Тест для создания производителя """
    api_client.force_authenticate(user=user_first)
    data = {
        "name": "Гамма",
        "email": "gamma@yandex.ru",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "Римского-Корсакова",
        "house_number": "54",
        "level": 0
    }
    response = api_client.post('/manufacturers/', data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_incorrect_lvl_manufacturer_api(api_client, user_first, jwt_token_for_first_user):
    """ Тест для создания производителя с некорректным уровнем
    error: 'Убедитесь, что это значение меньше либо равно 0.' """
    api_client.force_authenticate(user=user_first)
    data = {
        "name": "Гамма",
        "email": "gamma@yandex.ru",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "Римского-Корсакова",
        "house_number": "54",
        "level": 3
    }
    response = api_client.post('/manufacturers/', data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_manufacturer_api(api_client, user_first, jwt_token_for_first_user, first_manufacturer):
    """ Тест для изменения производителя """
    api_client.force_authenticate(user=user_first)
    data = {
        "name": "Гамма",
        "email": "gamma@yandex.ru",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "Римского-Корсакова",
        "house_number": "53",
        "level": 0
    }
    response = api_client.put(f'/manufacturers/{first_manufacturer.id}/', data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_manufacturer_api(api_client, user_first, jwt_token_for_first_user, first_manufacturer):
    """ Тест для удаления производителя """
    api_client.force_authenticate(user=user_first)
    response = api_client.delete(f'/manufacturers/{first_manufacturer.id}/')
    assert response.status_code == 204


# Тесты для работы с розничными сетями


@pytest.mark.django_db
def test_get_list_retail_network_api(api_client, user_first, jwt_token_for_first_user):
    """ Тест для получения списка розничных сетей """
    api_client.force_authenticate(user=user_first)
    response = api_client.get('/retail_networks/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_detail_retail_network_api(api_client, user_first, jwt_token_for_first_user, first_retail_network):
    """ Тест для получения розничной сети """
    api_client.force_authenticate(user=user_first)
    response = api_client.get(f'/retail_networks/{first_retail_network.id}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_retail_network_first_lvl_api(api_client, user_first, jwt_token_for_first_user, first_manufacturer):
    """ Тест для создания розничной сети """
    api_client.force_authenticate(user=user_first)
    data = {
        "manufacturer": first_manufacturer.id,
        "name": "Серебро",
        "email": "serebro@yandex.ru",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "ул Кржижановского",
        "house_number": "7",
        "level": 1
    }
    response = api_client.post('/retail_networks/', data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_retail_network_second_lvl_api(api_client, user_first, jwt_token_for_first_user, first_retail_network):
    """ Тест для создания розничной сети """
    api_client.force_authenticate(user=user_first)
    data = {
        "retail_network": first_retail_network.id,
        "name": "Серебро",
        "email": "serebro@yandex.ru",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "ул Кржижановского",
        "house_number": "7",
        "level": 2
    }
    response = api_client.post('/retail_networks/', data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_crete_retail_network_incorrect_second_lvl_api(api_client, user_first, jwt_token_for_first_user,
                                                       first_manufacturer):
    """ Тест для создания розничной сети с некорректным вторым уровнем
    error: 'Для второго уровня требуется закупаться у сетевого поставщика.'"""
    api_client.force_authenticate(user=user_first)
    data = {
        "manufacturer": first_manufacturer.id,
        "name": "Серебро",
        "email": "serebro@yandex.ru",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "ул Кржижановского",
        "house_number": "7",
        "level": 2
    }
    response = api_client.post('/retail_networks/', data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_crete_retail_network_incorrect_first_lvl_api(api_client, user_first, jwt_token_for_first_user,
                                                      first_retail_network):
    """ Тест для создания розничной сети с некорректным первым уровнем
    error: 'Для первого уровня требуется закупаться у завода-производителя.'"""
    api_client.force_authenticate(user=user_first)
    data = {
        "retail_network": first_retail_network.id,
        "name": "Серебро",
        "email": "serebro@yandex.ru",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "ул Кржижановского",
        "house_number": "7",
        "level": 1
    }
    response = api_client.post('/retail_networks/', data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_crete_retail_network_incorrect_lvl_api(api_client, user_first, jwt_token_for_first_user, first_retail_network,
                                                first_manufacturer):
    """ Тест для создания розничной сети с некорректным уровнем
    error: 'Выберите только одного поставщика: завод или розничную сеть.'"""
    api_client.force_authenticate(user=user_first)
    data = {
        "retail_network": first_retail_network.id,
        "manufacturer": first_manufacturer.id,
        "name": "Серебро",
        "email": "serebro@yandex.ru",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "ул Кржижановского",
        "house_number": "7",
        "level": 1
    }
    response = api_client.post('/retail_networks/', data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_retail_network_api(api_client, user_first, jwt_token_for_first_user,
                                second_retail_network, first_retail_network):
    """ Тест для изменения розничной сети """
    api_client.force_authenticate(user=user_first)
    data = {
        "retail_network": second_retail_network.id,
        "manufacturer": None,
        "name": "Серебро",
        "email": "serebro@yandex.ru",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "ул Кржижановского",
        "house_number": "12",
        "level": 2
    }
    response = api_client.put(f'/retail_networks/{first_retail_network.id}/', data=json.dumps(data),
                              content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_put_incorrect_lvl_network_api(api_client, user_first, jwt_token_for_first_user,
                                       first_manufacturer, first_retail_network, second_retail_network):
    """ Тест для изменения розничной сети с некорректным уровнем
    error: 'Выберите только одного поставщика: завод или розничную сеть.'"""
    api_client.force_authenticate(user=user_first)
    data = {
        "retail_network": second_retail_network.id,
        "manufacturer": first_manufacturer.id,
        "name": "Серебро",
        "email": "serebro@yandex.ru",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "ул Кржижановского",
        "house_number": "12",
        "level": 2
    }
    response = api_client.put(f'/retail_networks/{first_retail_network.id}/', data=json.dumps(data),
                              content_type='application/json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_retail_network_api(api_client, user_first, jwt_token_for_first_user, first_retail_network):
    """ Тест для удаления розничной сети """
    api_client.force_authenticate(user=user_first)
    response = api_client.delete(f'/retail_networks/{first_retail_network.id}/')
    assert response.status_code == 204


# Тесты на работу с ИП


@pytest.mark.django_db
def test_get_individual_entrepreneur_list_api(api_client, user_first, jwt_token_for_first_user):
    """ Тест для получения списка ИП """
    api_client.force_authenticate(user=user_first)
    response = api_client.get('/individual_entrepreneurs/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_detail_individual_entrepreneur_api(api_client, user_first, jwt_token_for_first_user,
                                                first_individual_entrepreneur):
    """ Тест для получения ИП """
    api_client.force_authenticate(user=user_first)
    response = api_client.get(f'/individual_entrepreneurs/{first_individual_entrepreneur.id}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_individual_entrepreneur_first_lvl_api(api_client, user_first, jwt_token_for_first_user,
                                                      first_manufacturer):
    """ Тест для создания ИП первый уровень"""
    api_client.force_authenticate(user=user_first)
    data = {
        "name": "Крис Кэтт",
        "email": "criscat@gmail.com",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "ул Чайковского",
        "house_number": "7",
        "level": 1,
        "manufacturer": first_manufacturer.id,
        "retail_network": None
    }
    response = api_client.post('/individual_entrepreneurs/', data=json.dumps(data),
                               content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_individual_entrepreneur_second_lvl_api(api_client, user_first, jwt_token_for_first_user,
                                                       first_retail_network):
    """ Тест для создания ИП второй уровень"""
    api_client.force_authenticate(user=user_first)
    data = {
        "name": "Крис Кэтт",
        "email": "criscat@gmail.com",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "ул Чайковского",
        "house_number": "7",
        "level": 2,
        "manufacturer": None,
        "retail_network": first_retail_network.id
    }
    response = api_client.post('/individual_entrepreneurs/', data=json.dumps(data),
                               content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_individual_entrepreneur_incorrect_lvl_api(api_client, user_first, jwt_token_for_first_user,
                                                          first_manufacturer):
    """ Тест для создания ИП с некорректным уровнем
    error: 'Для второго уровня требуется закупаться у сетевого поставщика.'"""
    api_client.force_authenticate(user=user_first)
    data = {
        "name": "Крис Кэтт",
        "email": "criscat@gmail.com",
        "country": "Россия",
        "city": "Санкт-Петербург",
        "street": "ул Чайковского",
        "house_number": "7",
        "level": 2,
        "manufacturer": first_manufacturer.id,
        "retail_network": None
    }
    response = api_client.post('/individual_entrepreneurs/', data=json.dumps(data),
                               content_type='application/json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_individual_entrepreneur_api(api_client, user_first, jwt_token_for_first_user,
                                            first_individual_entrepreneur):
    """ Тест для удаления ИП """
    api_client.force_authenticate(user=user_first)
    response = api_client.delete(f'/individual_entrepreneurs/{first_individual_entrepreneur.id}/')
    assert response.status_code == 204


# Тесты на работу с продуктами

@pytest.mark.django_db
def test_get_product_list_api(api_client, user_first, jwt_token_for_first_user):
    """ Тест для получения списка продуктов """
    api_client.force_authenticate(user=user_first)
    response = api_client.get('/products/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_product_detail_api(api_client, user_first, jwt_token_for_first_user, first_product):
    """ Тест для получения продукта """
    api_client.force_authenticate(user=user_first)
    response = api_client.get(f'/products/{first_product.id}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_product_api(api_client, user_first, jwt_token_for_first_user, first_manufacturer):
    """ Тест для создания продукта """
    api_client.force_authenticate(user=user_first)
    data = {
        "name": "Набор пастели акварельной",
        "model": "Акварельная пастель",
        "release_date": "2024-02-20",
        "owner": user_first.id,
        "manufacturer": first_manufacturer.id,
        "retailers": None,
        "entrepreneurs": None,
    }
    response = api_client.post('/products/', data=json.dumps(data),
                               content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_product_api(api_client, user_first, jwt_token_for_first_user, first_product):
    """ Тест для обновления продукта """
    api_client.force_authenticate(user=user_first)
    data = {
        "name": "Набор пастели акварельной",
        "model": "Пастель",
        "release_date": "2024-02-20",
        "owner": first_product.owner.id,
        "manufacturer": first_product.manufacturer.id,
        "retailers": None,
        "entrepreneurs": None,
    }
    response = api_client.put(f'/products/{first_product.id}/', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_product_api(api_client, user_first, jwt_token_for_first_user, first_product):
    """ Тест для удаления продукта """
    api_client.force_authenticate(user=user_first)
    response = api_client.delete(f'/products/{first_product.id}/')
    assert response.status_code == 204


# Тесты на работу с транзакциями


@pytest.mark.django_db
def test_get_transaction_list_api(api_client, user_first, jwt_token_for_first_user):
    """ Тест для получения списка транзакций """
    api_client.force_authenticate(user=user_first)
    response = api_client.get('/transactions/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_transaction_detail_api(api_client, user_first, jwt_token_for_first_user, first_transaction):
    """ Тест для получения транзакции """
    api_client.force_authenticate(user=user_first)
    response = api_client.get(f'/transactions/{first_transaction.id}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_transaction_api(api_client, user_first, jwt_token_for_first_user, first_product, first_manufacturer,
                                 first_individual_entrepreneur):
    """ Тест для создания транзакции """
    api_client.force_authenticate(user=user_first)
    data = {
        "product": first_product.id,
        "seller_manufacturer": first_manufacturer.id,
        "seller_retail_network": None,
        "seller_individual_entrepreneur": None,
        "buyer_manufacturer": None,
        "buyer_retail_network": None,
        "buyer_individual_entrepreneur": first_individual_entrepreneur.id,
        "amount": 10,
        "debt": "20000.00",
    }
    response = api_client.post('/transactions/', data=json.dumps(data),
                               content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_incorrect_transaction_two_sellers_api(api_client, user_first, jwt_token_for_first_user, first_product,
                                          first_retail_network, first_individual_entrepreneur, first_manufacturer):
    """ Тест для создания некорректной транзакции
    error: 'Выберите только одно поле продавца.'"""
    api_client.force_authenticate(user=user_first)
    data = {
        "product": first_product.id,
        "seller_manufacturer": first_manufacturer.id,
        "seller_retail_network": first_retail_network.id,
        "seller_individual_entrepreneur": None,
        "buyer_manufacturer": None,
        "buyer_retail_network": None,
        "buyer_individual_entrepreneur": first_individual_entrepreneur.id,
        "amount": 10,
        "debt": "20000.00",
    }
    response = api_client.post('/transactions/', data=json.dumps(data),
                               content_type='application/json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_create_incorrect_transaction_two_buyers_api(api_client, user_first, jwt_token_for_first_user, first_product,
                                          first_retail_network, first_individual_entrepreneur, first_manufacturer):
    """ Тест для создания некорректной транзакции
    error: 'Выберите только одно поле покупателя.'"""
    api_client.force_authenticate(user=user_first)
    data = {
        "product": first_product.id,
        "seller_manufacturer": None,
        "seller_retail_network": first_retail_network.id,
        "seller_individual_entrepreneur": None,
        "buyer_manufacturer": first_manufacturer.id,
        "buyer_retail_network": None,
        "buyer_individual_entrepreneur": first_individual_entrepreneur.id,
        "amount": 10,
        "debt": "20000.00",
    }
    response = api_client.post('/transactions/', data=json.dumps(data),
                               content_type='application/json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_transaction_api(api_client, user_first, jwt_token_for_first_user, first_transaction):
    """ Тест для удаления транзакции """
    api_client.force_authenticate(user=user_first)
    response = api_client.delete(f'/transactions/{first_transaction.id}/')
    assert response.status_code == 204