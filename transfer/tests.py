import datetime
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .views import TransactionViewSet
from .models import Utilzer, BankAccount
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



    return utilzers, bankaccounts


class AmountApiTestCase(APITestCase):

    def setUp(self):
        self.utilzers, self.bankaccounts = fill_db()

    def test_create_transaction(self):
        factory = APIRequestFactory()
        request = factory.post('/transaction/transmiting/', {'account_from': ['account1', 'account2'], 'account_to': 'account5', 'amount_for_transmitting': 30})
        view = TransactionViewSet.as_view({'post': 'transmiting'})

        force_authenticate(request, user=self.utilzers[0])
        response = view(request)
        self.assertEqual(response.data['name_from'], self.utilzers[0].name)
        self.assertEqual(response.data['name_to'], self.utilzers[2].name)
        self.assertEqual(response.data['total_quantum'], "30.00")
        self.assertEqual(response.data['is_canceled'], False)

