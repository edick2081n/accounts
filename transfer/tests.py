from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .views import BankAccountViewSet, TransactionViewSet
from .models import Utilzer, BankAccount, Amount, Transaction
import datetime
import json


def fill_db():
    utilzers = []
    utilzers.append(Utilzer.objects.create(name='utilzer1',
                                           username='utilzer1',
                                           password=111 ))
    utilzers.append(Utilzer.objects.create(name='utilzer2',
                                           username='utilzer2',
                                           password=111))
    utilzers.append(Utilzer.objects.create(name='utilzer3',
                                           username='utilzer3',
                                           password=111))

    bankaccounts=[]
    bankaccounts.append(BankAccount.objects.create(name='account1',
                                           balance= 1000,
                                           account_of_utilzer=utilzers[0]))
    bankaccounts.append(BankAccount.objects.create(name='account2',
                                                   balance=2000,
                                                   account_of_utilzer=utilzers[0]))
    bankaccounts.append(BankAccount.objects.create(name='account3',
                                                   balance=1300,
                                                   account_of_utilzer=utilzers[1]))
    bankaccounts.append(BankAccount.objects.create(name='account4',
                                                   balance=1500,
                                                   account_of_utilzer=utilzers[1]))

    bankaccounts.append(BankAccount.objects.create(name='account5',
                                                   balance=3500,
                                                   account_of_utilzer=utilzers[2]))
    bankaccounts.append(BankAccount.objects.create(name='account6',
                                                   balance=5500,
                                                   account_of_utilzer=utilzers[2]))

    # amounts=[]
    # amounts.append(Amount.objects.create(amount_from_account='account1',
    #                                      amount_to_account='account5',
    #                                      quantum=50,
    #                                      datetime= datetime.datetime.now(),
    #                                      transaction=1))
    # amounts.append(Amount.objects.create(amount_from_account='account2',
    #                                      amount_to_account='account5',
    #                                      quantum=50,
    #                                      datetime=datetime.datetime.now(),
    #                                      transaction=1))
    # amounts.append(Amount.objects.create(amount_from_account='account3',
    #                                      amount_to_account='account5',
    #                                      quantum=25,
    #                                      datetime=datetime.datetime.now(),
    #                                      transaction=2))
    # amounts.append(Amount.objects.create(amount_from_account='account4',
    #                                      amount_to_account='account5',
    #                                      quantum=25,
    #                                      datetime=datetime.datetime.now(),
    #                                      transaction=2))
    #
    # transactions = []
    # transactions.append(Transaction.objects.create(name_from='utilzer1',
    #                                      name_to ='utilzer3',
    #                                      total_quantum=100,
    #                                      datetime= datetime.datetime.now()))
    # transactions.append(Transaction.objects.create(name_from='utilzer2',
    #                                      name_to='utilzer3',
    #                                      total_quantum= 50,
    #                                      datetime=datetime.datetime.now()))



### ВОПРОС К ВИТАЛИЮ Я ДОЛЖЕН УКАЗАТЬ В ЯВНОМ ВИДЕ ВСЕ ПОЛЯ МОДЕЛИ ИНАЧЕ КАК МНЕ СОЗДАТЬ ОБЬЕКТ НО КАК ТОГДА ПРОВЕРИТЬ ССЫЛОЧНУЮ ЦЕЛОСТНОСТЬ
### МЕЖДУ МОДЕЛЯМИ В ЧАСТИЕ КЛЮЧЕЙ   ForeignKey(



    return utilzers, bankaccounts
    #     amounts, transactions


# Using the standard RequestFactory API to create a form POST request
class BankAccountsApiTestCase(APITestCase):
    def setUp(self):
        self.utilzers, self.bankaccounts = fill_db()
        token = Token.objects.create(user=self.utilzers[0])
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
#
    def test_get_bankaccount(self):
        response = self.client.get('/api/bankaccounts/', format='json')
        data=json.loads(json.dumps(response.data))
        for account in self.bankaccounts:
            if account.account_of_utilzer.name!=self.utilzers[0].name:
                self.assertIn({'account_of_utilzer': account.account_of_utilzer.name, 'name':account.name}, data)

### написать тесты на создание счета , обновление счета, на получение информации об одном счете
class AmountApiTestCase(APITestCase):

    def setUp(self):
        self.utilzers, self.bankaccounts = fill_db()
        # token = Token.objects.create(user=self.utilzers[0])
        # self.client = APIClient()
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


    def test_create_transaction(self):
        factory = APIRequestFactory()
        request = factory.post('/transaction/transmiting/', {'account_from': ['account1', 'account2'], 'account_to': 'account5', 'amount_for_transmitting': 30})
        view = TransactionViewSet.as_view({'post': 'transmiting'})

        force_authenticate(request, user=self.utilzers[0])
        response = view(request)
      # print(response.data)
        self.assertEqual(response.data['name_from'], self.utilzers[0].name)
