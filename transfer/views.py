
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Utilzer, BankAccount, Amount, Transaction
from .serializers import UtilzerSerializer, BankAccountSerializer, AmountSerializer, DetailUtilzerSerializer, \
    TokenSerializer, LoginSerializer, TransactionSerializer
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





class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(methods=['POST'], detail=True)
    def transmiting(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)







