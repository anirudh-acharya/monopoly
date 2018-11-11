# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from banker.models import Game, Player, Account, Transaction


class SignalTestCases(TestCase):

    def setUp(self):
        game = Game.objects.create()

        person_one = User.objects.create(id=1, username='person_one')
        person_two = User.objects.create(id=2, username='person_two')

        player_one = Player.objects.create(person_id=1)
        player_two = Player.objects.create(person_id=2)

        self.account_one = Account.objects.create(game=game,
                                                  player=player_one,
                                                  balance=1500)

        self.account_two = Account.objects.create(game=game,
                                                  player=player_two,
                                                  balance=1500)

    def test_update_account_balance_signal_for_transaction_creation(self):
        self.transaction = Transaction.objects.create(payer_account=self.account_one,
                                                      payee_account=self.account_two,
                                                      amount=200,
                                                      description='test transaction'
                                                      )

        self.assertEquals(self.account_one.balance, 1300)
        self.assertEquals(self.account_two.balance, 1700)

    def test_update_account_balance_signal_for_transaction_update(self):
        self.transaction = Transaction.objects.create(payer_account=self.account_one,
                                                      payee_account=self.account_two,
                                                      amount=200,
                                                      description='test transaction'
                                                      )

        self.transaction.amount = 100
        self.transaction.save()

        self.assertEquals(self.account_one.balance, 1200)
        self.assertEquals(self.account_two.balance, 1800)
