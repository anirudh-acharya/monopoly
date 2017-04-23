# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Transaction(models.Model):
    payer = models.ForeignKey(User, related_name='payer')
    payee = models.ForeignKey(User, related_name='payee')
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=255)


    def __str__(self):
        return "%s paid %s rupees to %s. Remarks: %s" % (
                self.payer.first_name,
                str(self.amount),
                self.payee.first_name,
                self.description)
