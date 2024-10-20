from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bank_accounts.views import BankAccountViewSet

# Create a router and register the BankAccountViewSet
router = DefaultRouter()
router.register(r'bank_accounts', BankAccountViewSet, basename='bankaccount')

urlpatterns = [
    path('api/', include(router.urls)),  # Include the router URLs
]
