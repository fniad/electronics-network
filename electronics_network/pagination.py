""" Пагинаторы приложения users """
from rest_framework.pagination import PageNumberPagination


class ManufacturerPagination(PageNumberPagination):
    """ Пагинатор для вывода заводов """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class RetailNetworkPagination(PageNumberPagination):
    """ Пагинатор для вывода розничных сетей"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class IndividualEntrepreneurPagination(PageNumberPagination):
    """ Пагинатор для вывода ИП """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class ProductPagination(PageNumberPagination):
    """ Пагинатор для вывода продуктов """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class TransactionPagination(PageNumberPagination):
    """ Пагинатор для вывода транзакции """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50
