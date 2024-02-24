from django.urls import path, include
from rest_framework.routers import DefaultRouter
from electronics_network.views import (ProductViewSet, ManufacturerViewSet, RetailNetworkViewSet,
                                       IndividualEntrepreneurViewSet, TransactionViewSet)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'retail_networks', RetailNetworkViewSet, basename='retail_network')
router.register(r'individual_entrepreneurs', IndividualEntrepreneurViewSet, basename='individual_entrepreneur')
router.register(r'transactions', TransactionViewSet, basename='transaction')


urlpatterns = [
    path('', include(router.urls)),
]
