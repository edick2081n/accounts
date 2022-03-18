from rest_framework.routers import DefaultRouter
from transfer import views

router = DefaultRouter()
router.register('auth', views.LoginUtilzerViewSet)
router.register('clients', views.UtilzerViewSet, basename='clients')
router.register('transaction', views.TransactionViewSet,  basename='accounts')
router.register('amount', views.ListAmountViewSet, basename='list')
router.register('detailbankaccount', views.DetailBankAccountViewSet, basename='detail')
router.register('delete', views.DeleteTransactionViewSet, basename='del')







