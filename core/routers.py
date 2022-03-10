from rest_framework.routers import DefaultRouter
from transfer import views

router = DefaultRouter()
router.register('auth', views.LoginUtilzerViewSet)
router.register('clients', views.UtilzerViewSet, basename='clients')
router.register('transaction', views.TransactionViewSet,  basename='accounts')
router.register('bankaccounts', views.BankAccountViewSet, basename='bankaccounts')







