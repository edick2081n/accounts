from django.db import models
from django.contrib.auth.models import AbstractUser


class Utilzer(AbstractUser):
    """
    модель пользователя
    """

    name = models.CharField(max_length=100)
    """имя пользователя"""

    def __str__(self):
        """
        строковое предствление обьекта пользователя
        :return: имя пользователя
        """
        return self.name

class BankAccount(models.Model):
    """
    модель счета
    """
    name = models.CharField(max_length=100)
    """название(номер) счета"""
    balance = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    """текущий остаток по счету"""
    account_of_utilzer = models.ForeignKey(Utilzer, on_delete=models.PROTECT)
    """пользователь(:class:`Utilzer`) к которому относится данный счет """

    class Meta:
        unique_together = ('name', 'account_of_utilzer')


    def __str__(self):
        """
        строковое представление обьекта счета
        :return: название счета
        """
        return self.name


class Amount(models.Model):
    """
    модель суммы перевода
    """
    amount_from_account = models.ForeignKey(BankAccount, related_name='amount_from_account', on_delete=models.PROTECT)
    """счет списания средств(:class:`Bank_Account`) к которому относится данная сумма перевода """
    amount_to_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    """счет зачисления средств(:class:`Bank_Account`) к которому относится данная сумма перевода """
    quantum = models.DecimalField(max_digits=16, decimal_places=2)
    """сумма переводимых средств"""
    datetime = models.DateTimeField(auto_created=True)
    """дата и время транзакции"""

    def __str__(self):
        """
        строковое представление обьекта суммы перевода
        :return: сумма переведенных средств
        """
        return self.quantum