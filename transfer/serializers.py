from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from .models import Utilzer, BankAccount, Amount


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']

class LoginSerializer(serializers.Serializer):

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

    class Meta:
        model = Utilzer
        fields = ['username', 'password']




class BankAccountSerializer(serializers.ModelSerializer):
    account_of_utilzer = serializers.StringRelatedField()
    class Meta:
        model = BankAccount
        exclude = ['balance']


class DetailUtilzerSerializer(UtilzerSerializer):
    bankaccount_set = BankAccountSerializer(many=True, required=False)

    class Meta(UtilzerSerializer.Meta):

        fields = ['username', 'bankaccount_set']






class AmountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amount
        fields = "__all__"

class TransactionSerializer(serializers.Serializer):

    amount_from_accounts = serializers.ListField(child=serializers.CharField())
    amount_to_account = serializers.CharField()
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)

    def save(self):
        accounts_from = self.validated_data['amount_from_accounts']


