from django.contrib import admin

from transfer.models import Utilzer, BankAccount, Amount, Transaction

admin.site.register(Utilzer)
admin.site.register(BankAccount)
admin.site.register(Amount)
admin.site.register(Transaction)
