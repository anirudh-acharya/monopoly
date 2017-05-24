# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Transaction


@receiver(post_save, sender=Transaction)
def update_account_balance(sender, **kwargs):
    """
    Updates the account balance of the payer and the payee of the transaction
    """
    print kwargs

