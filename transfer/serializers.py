from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.fields import DateField

from .models import Utilzer, BankAccount, Amount, Transaction
from rest_framework.response import Response
from django.db.models.fields import DateField

class TokenSerializer(serializers.ModelSerializer):
    """сериализатор токена авторизации польззователя"""
    class Meta:
        model = Token
        fields = ['key']

class LoginSerializer(serializers.Serializer):
    """сериализатор авторизационнх данных пользователя"""
    username = serializers.CharField(min_length=1, max_length =200)
    password = serializers.CharField(min_length=1, max_length=150)

    def validate(self, raw_data):    # нужно реализовать сравнение паролей

        user_username = raw_data.get('username')
        user_password = raw_data.get('password')
        if not user_username or not user_password:
            raise serializers.ValidationError(' both fields are requaired')
        self.check_registration(raw_data)    #  мы вызываем метод объекта сериализатора (который мы описываем ниже)
        return raw_data

    def check_registration(self, validated_data):
        user_username = validated_data.get('username')
        user_password = make_password(validated_data.get('password'))
        try:
            user_instance = Utilzer.objects.get(username=user_username)
        except Utilzer.DoesNotExist:
            raise serializers.ValidationError(' user in not found')

        if user_instance.password == user_password:
            raise serializers.ValidationError('password in incorrect')
        self.instance = user_instance  # полю обьекта сериализатора (LoginSerializer) который мы в дальнейшем
                                       # использу

class UtilzerSerializer(serializers.ModelSerializer):
    """сериализатор данных пользователя"""
    class Meta:
        model = Utilzer
        fields = ['username', 'password']




class BankAccountSerializer(serializers.ModelSerializer):
    """сериализатор данных о счетах принадлежащих пользователю"""
    account_of_utilzer = serializers.StringRelatedField()

    class Meta:
        model = BankAccount
        fields = ['account_of_utilzer', 'name']


class DetailUtilzerSerializer(UtilzerSerializer):
    """

    """
   # bankaccount_set = BankAccountSerializer(many=True, required=False)
    bankaccount_set = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta(UtilzerSerializer.Meta):

        fields = ['username', 'bankaccount_set']






class AmountSerializer(serializers.ModelSerializer):
    """сериализатор данных о произведенных перечислениях средств
       со счета даннго пользователя на счет получателя средств
    """
    amount_from_account_name = serializers.StringRelatedField(source='amount_from_account')


    class Meta:
        model = Amount
        fields = "__all__"

class TransmittingSerializer(serializers.Serializer):
    """сериализатор данных о произведенной транзакции со счетов даннго пользователя
       на счет получателя средств
    """
    account_from = serializers.ListField(child=serializers.CharField())
    account_to = serializers.CharField()
    amount_for_transmitting = serializers.DecimalField(max_digits=16, decimal_places=2)

    def validate(self, data):
        account_from = data['account_from']
        amount_for_transmitting = data['amount_for_transmitting']
        amount_for_transmitting_from_account = amount_for_transmitting / len(account_from)
        if BankAccount.objects.filter(name__in=account_from,
                                      balance__gte=amount_for_transmitting_from_account).count() != len(account_from):
            raise serializers.ValidationError('недостаток средств на одном из счетов')
        return data

    def save(self):
        account_from = self.validated_data['account_from']
        account_to = self.validated_data['account_to']
        amount_for_transmitting = self.validated_data['amount_for_transmitting']
        utilzer_from = BankAccount.objects.get(name=account_from[0]).account_of_utilzer
        object_bankaccount_to = BankAccount.objects.get(name=account_to)
        utilzer_to =object_bankaccount_to.account_of_utilzer
        amount_for_transmitting_from_account = amount_for_transmitting / len(account_from)


        object_transaction = Transaction.objects.create(total_quantum=amount_for_transmitting,
                                                         name_from=utilzer_from,
                                                         name_to=utilzer_to)


        for account in account_from:
            object_bankaccount_from = BankAccount.objects.get(name=account)
            object_bankaccount_from_balance = object_bankaccount_from.balance


            new_balance_for_account_from = object_bankaccount_from_balance - amount_for_transmitting_from_account


            object_amount = Amount.objects.create(amount_from_account=object_bankaccount_from,
                                                  amount_to_account=object_bankaccount_to,
                                                  quantum=amount_for_transmitting_from_account,
                                                  transaction=object_transaction)
            object_bankaccount_from.balance = new_balance_for_account_from
            object_bankaccount_from.save()



        object_bankaccount_to.balance+=amount_for_transmitting
        object_bankaccount_to.save()
        return object_transaction


class TransactionSerializer(serializers.ModelSerializer):
    """сериализатор данных о произведенных транзакциях
    """
    name_from = serializers.StringRelatedField()
    name_to = serializers.StringRelatedField()
    class Meta:
        model = Transaction
        fields = '__all__'



class DetailBankAccountSerializer(BankAccountSerializer):
    """сериализатор данных о произведенных
    """
    list_amount_from = AmountSerializer(many=True, required=False)

    class Meta(BankAccountSerializer.Meta):

        #fields = {'name':['exact'], 'list_amount_from':['exact', 'contains']}
        fields = ['name', 'balance', 'list_amount_from']


