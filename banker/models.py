# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


class Player(models.Model):
    person = models.ForeignKey(User)

    def __str__(self):
        return self.person.__str__()


class Game(models.Model):
    players = models.ManyToManyField(Player, through='Account')
    start_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Account(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    balance = models.IntegerField()

    class Meta:
        unique_together = ('game', 'player',)

    def __str__(self):
        return "Game: %s Player: %s" % (str(self.game), str(self.player))


class Transaction(models.Model):
    payer_account = models.ForeignKey(Account, related_name='payer_account')
    payee_account = models.ForeignKey(Account, related_name='payee_account')
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return "%s paid %s rupees to %s. Remarks: %s" % (
                self.payer.first_name,
                str(self.amount),
                self.payee.first_name,
                self.description)

