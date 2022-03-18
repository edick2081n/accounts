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
    name = models.CharField(max_length=100, unique=True)
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
    amount_from_account = models.ForeignKey(BankAccount, related_name='list_amount_from', on_delete=models.PROTECT)
    """счет списания средств(:class:`Bank_Account`) к которому относится данная сумма перевода """
    amount_to_account = models.ForeignKey(BankAccount, related_name='list_amount_to', on_delete=models.PROTECT)
    """счет зачисления средств(:class:`Bank_Account`) к которому относится данная сумма перевода """
    quantum = models.DecimalField(max_digits=16, decimal_places=2)
    """сумма переводимых средств"""
    datetime = models.DateTimeField(auto_now_add=True)
    """дата и время транзакции"""
    transaction = models.ForeignKey('Transaction',related_name='list_amount', on_delete=models.PROTECT)
    """дата и время транзакции"""
    def __str__(self):
        """
        строковое представление обьекта суммы перевода
        :return: сумма средств переведенных с данного счета
        """
        return self.quantum


class Transaction(models.Model):
    """
    модель транзакции, включающей в себя несколько сумм переводимых с нескольких счетов на один счет получателя
    """

    name_from = models.ForeignKey(Utilzer, related_name='list_transaction_from', on_delete=models.PROTECT)
    """имя пользователя который перечисляет средства"""
    name_to = models.ForeignKey(Utilzer, related_name='list_transaction_to', on_delete=models.PROTECT)
    """имя пользователя которому перечисляют средства"""
    total_quantum = models.DecimalField(max_digits=16, decimal_places=2)
    """общая сумма переводимых средств"""
    datetime = models.DateTimeField(auto_now_add=True)
    """дата и время создания обьекта транзакции"""
    is_canceled= models.BooleanField(default=False)
    """параметр отвечающий за использование транзакции при ее отмене"""

    class Meta:
        unique_together = ('name_from', 'name_to', 'total_quantum', 'datetime')

    def __str__(self):
        """
        строковое предствление обьекта транзакции
        :return: общая сумма средств переведенного между пользователями в данный момент времени
        """
        return self.total_quantum