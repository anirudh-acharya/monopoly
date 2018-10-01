# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from banker.models import Transaction


@receiver(post_save, sender=Transaction)
def update_account_balance_before_transaction_save(sender, **kwargs):
    """
    Updates the account balance of the payer and the payee of the transaction
    """

    transaction = kwargs['instance']

    payer_account = transaction.payer_account
    payee_account = transaction.payee_account

    payer_account.balance = F('balance') - transaction.amount
    payee_account.balance = F('balance') + transaction.amount

    payer_account.save()
    payee_account.save()

    payer_account.refresh_from_db()
    payee_account.refresh_from_db()
