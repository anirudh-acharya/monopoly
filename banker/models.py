# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Player(models.Model):
    person = models.ForeignKey(User)

    def __str__(self):
        return self.person.__str__()


class Game(models.Model):
    players = models.ManyToManyField(Player, through='Account')
    start_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Game: %s" % str(self.id)


class Account(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    balance = models.IntegerField()

    class Meta:
        unique_together = ('game', 'player',)

    def __str__(self):
        return str(self.player)


class Transaction(models.Model):
    payer_account = models.ForeignKey(Account, related_name='payer_account')
    payee_account = models.ForeignKey(Account, related_name='payee_account')
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        msg = "%s paid to %s %d." % (
                self.payer_account.player.person.username,
                self.payee_account.player.person.username,
                self.amount)
        if self.description:
            msg += " Remarks: %s" % (self.description)

        return msg

    def clean(self):
        if self.payer_account.balance < self.amount:
            raise ValidationError(_('Payer account balance is not sufficient to complete this transaction, short by %d' % (
                        self.amount - self.payer_account.balance)))

        if self.payer_account.id == self.payee_account_id:
            raise ValidationError(_('Payer and payee account must not be same'))
