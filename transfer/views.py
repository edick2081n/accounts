
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Utilzer, BankAccount, Amount, Transaction
from .serializers import UtilzerSerializer, BankAccountSerializer, AmountSerializer, DetailUtilzerSerializer, \
    TokenSerializer, LoginSerializer, TransmittingSerializer, TransactionSerializer, DetailBankAccountSerializer, \
    DeleteTransactionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend


class LoginUtilzerViewSet(viewsets.GenericViewSet):
    """
    эндпоинт авторизации пользователя
    """
    queryset = Token.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
     #   """"обработчик запросов авторизации"""

       input_serializer = LoginSerializer(data=request.data)
       input_serializer.is_valid(raise_exception=True)

       user = input_serializer.instance
       token, _ = Token.objects.get_or_create(user=user)   # применен метод  get_or_create который возвращает кортеж нас интересует только перрый член кортежа поэтому добалвляем подчеркивание в качестве второго члена кортежа

       return Response({'token': token.key})



class UtilzerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    вьюсет предоставляет информацию обо всех пользователях за исключением суперпользователля
    """
    serializer_class = DetailUtilzerSerializer
    pagination_class = None
    def get_queryset(self):

        return Utilzer.objects.exclude(is_superuser=True)


class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    вьюсет предоставляет информацию обо всех счетах всех пользователей
    """
   # queryset = BankAccount.objects.all()
    pagination_class = None
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        return BankAccount.objects.exclude(account_of_utilzer=self.request.user)
        #return BankAccount.objects.all()





class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    вьюсет предоставляет информацию о совершенной  транзаакции и позволяет создавать транзакцию
    (перевод средств с нескольких
    счетов данного пользователя на выбранный счет иного пользователя
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = None
    @action(methods=['POST'], detail=False)
    def transmiting(self, request):
        serializer = TransmittingSerializer(data=request.data)
        if serializer.is_valid():
            transaction=serializer.save()
            data = TransactionSerializer(transaction).data
            return Response(data)
        return Response(serializer.errors)


class ListTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    вьюсет предоставляет информацию о списке совершенных транзакций
     с возможностью сортировки по имени получателя  средств, общей сумме транзакции
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['total_quantum', 'name_to__name']

class ListAmountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    вьюсет предоставляет информацию о списке совершенных перечислений средств с выбранного
    счета конкретного пользователя на выбранный счет иного пользователя
    с возможностью сортировки по имени отправителя средств, диапазону дат, сумме
    """
    queryset = Amount.objects.all()
    serializer_class = AmountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'amount_from_account__name':['iexact'], 'quantum':['exact'], 'datetime':['gte', 'lte', 'exact', 'gt', 'lt']}


class DetailBankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    вьюсет предоставляет детализированную информацию о данном счете
    суммах перечислений средств, именах получателей средств, названий счетов получателей
    """
    queryset = BankAccount.objects.all()
    serializer_class = DetailBankAccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'list_amount_from']





class DeleteTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
