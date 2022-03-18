from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Utilzer, BankAccount, Amount, Transaction
from .serializers import AmountSerializer, DetailUtilzerSerializer, \
    TokenSerializer, LoginSerializer, TransmittingSerializer, TransactionSerializer, DetailBankAccountSerializer
from rest_framework.permissions import AllowAny
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
        """обработчик запросов авторизации
        """
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
    """
        вьюсет предоставляет информацию о новой транзакции созданной
        в результатет отмены ранее совершенной транзакции
    """
    queryset = Transaction.objects.all()
    pagination_class = None

    @action(methods=['POST'], detail=False)
    def returning(self, request):
        transaction_number = request.POST["transaction_number"]
        transaction_number = int(transaction_number)
        object_transaction_for_deleting = Transaction.objects.get(id=transaction_number)
        if object_transaction_for_deleting.is_canceled==True:
            return Response('возврат по данной транзакции невозможен')

        object_transaction = Transaction.objects.create(name_from=object_transaction_for_deleting.name_to,
                                                        name_to=object_transaction_for_deleting.name_from,
                                                        total_quantum=object_transaction_for_deleting.total_quantum)
        # Для простоты будем возвращать средства на счета отправителя не анализирую набор счетов с которых
        # эти средства были первоначально отправлены

        objects_bankaccount_for_return_money = BankAccount.objects.filter(account_of_utilzer=object_transaction.name_to)
        amounts_from_transaction = Amount.objects.filter(transaction=object_transaction_for_deleting)

        # так как любой amount в рамках данной транзакции ссылается на одну ту же транзакцию то можно взять любой amount
        # и взять из него номер счета на который переводились деньги

        object_bankaccount_from_return_money =amounts_from_transaction[0].amount_to_account
        object_bankaccount_to_return_money =amounts_from_transaction[0].amount_from_account
        quantity_accounts = len(objects_bankaccount_for_return_money)
        amount_for_returning = object_transaction.total_quantum / quantity_accounts
        if object_bankaccount_from_return_money.balance<object_transaction.total_quantum:
            return Response('для отмены данной транзакции у  получателя платежа не хватает средств на счете')
        else:
            for object_bankaccount in objects_bankaccount_for_return_money:
                object_bankaccount_new_balance = object_bankaccount.balance - amount_for_returning
                object_bankaccount.balance=object_bankaccount_new_balance
                object_bankaccount.save()
                object_amount = Amount.objects.create(amount_from_account=object_bankaccount_from_return_money,
                                                      amount_to_account=object_bankaccount,
                                                      quantum=amount_for_returning,
                                                      transaction=object_transaction_for_deleting)
            objects_bankaccount_from_return_money_balance = object_bankaccount_from_return_money.balance - object_transaction.total_quantum
            object_bankaccount_to_return_money.balance = objects_bankaccount_from_return_money_balance
            object_bankaccount_to_return_money.save()
            object_transaction_for_deleting.is_canceled=True
            object_transaction_for_deleting.save()
            data = TransactionSerializer(object_transaction).data
            return Response(data)













