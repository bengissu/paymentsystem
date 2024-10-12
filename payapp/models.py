from django.db import models
from django.contrib.auth.models import User


# Create your models here.

def get_account_default(currency):
    if currency == "usd":
        return 1243.5
    elif currency == "gbp":
        return 1000
    elif currency == "eur":
        return 1120.52
    else:
        return 0


class Account(models.Model):
    """
    Users bank accounts in different currencies.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CURRENCY_TYPES = (
        ("usd", "usd"),
        ("gbp", "gbp"),
        ("eur", "eur"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    currency = models.CharField(choices=CURRENCY_TYPES, max_length=3)
    # could be int if we think it as pennies but decimal field is more appropriate for banking operations
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=get_account_default)

    @property
    def full_name(self):
        """Return the full name of the account owner."""
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        return f"{self.full_name} ({self.currency})"


class TransferMoney(models.Model):
    """
    All transfers between users.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transfers_sent")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transfers_received")
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.from_user.account.full_name} sent {self.amount} {self.from_user.account.currency} to {self.to_user.account.full_name}."


class RequestMoney(models.Model):
    """
    All money requests between users.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_sent')
    requestee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_received')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    accepted_at = models.DateTimeField(null=True)
    declined_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.requester.account.full_name} requested {self.amount} {self.requester.account.currency} from {self.requestee.account.full_name}."
