
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Utilzer, BankAccount, Amount
from .serializers import UtilzerSerializer, BankAccountSerializer, AmountSerializer, DetailUtilzerSerializer, \
    TokenSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token


class LoginUtilzerViewSet(viewsets.GenericViewSet):
    queryset = Token.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
       input_serializer = LoginSerializer(data=request.data)
       input_serializer.is_valid(raise_exception=True)

       user = input_serializer.instance
       token, _ = Token.objects.get_or_create(user=user)   # применен метод  get_or_create который возвращает кортеж нас интересует только перрый член кортежа поэтому добалвляем подчеркивание в качестве второго члена кортежа

       return Response({'token': token.key})



class UtilzerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DetailUtilzerSerializer

    def get_queryset(self):

        return Utilzer.objects.exclude(is_superuser=True)


class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BankAccountSerializer
   # queryset = BankAccount.objects.all()
    def get_queryset(self):
        return BankAccount.objects.exclude(account_of_utilzer=self.request.user)
        #return BankAccount.objects.exclude(account_of_utilzer=self.request.user)
        #return BankAccount.objects.filter(account_of_utilzer='admin')





class DetailUtilzerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BankAccount.objects.all()

    serializer_class = DetailUtilzerSerializer

    @action(methods=['GET'], detail=True)
    def transmiting(self, request, *args, **kwargs):
        serializer = AmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount_from_account = serializer.validated_data['amount_from_account']
        amount_to_account = serializer.validated_data['amount_to_account']
        quantum = serializer.validated_data['quantum']
        object_amount = Amount.objects.create(amount_from_account=amount_from_account, amount_to_account=amount_to_account, quantum=quantum)

        return Response(object_amount.id)


