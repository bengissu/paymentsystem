from django.contrib import admin

from .models import Account, TransferMoney, RequestMoney

# Register your models here.

admin.site.register(Account)
admin.site.register(TransferMoney)
admin.site.register(RequestMoney)
