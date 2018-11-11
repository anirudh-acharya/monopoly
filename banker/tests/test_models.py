# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from banker.models import Game, Player, Account, Transaction


class ModelTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create()

        self.person_one = User.objects.create(id=1, username='person_one')
        self.person_two = User.objects.create(id=2, username='person_two')

        self.player_one = Player.objects.create(person_id=1)
        self.player_two = Player.objects.create(person_id=2)

        self.account_one = Account.objects.create(game=self.game,
                                                  player=self.player_one,
                                                  balance=1500)

        self.account_two = Account.objects.create(game=self.game,
                                                  player=self.player_two,
                                                  balance=1500)

    def test__str__game(self):
        game_time_created = self.game.start_time
        self.assertEquals("Game: 1", str(self.game))

    def test__str__player(self):
        self.assertEquals("person_one", str(self.player_one))

    def test__str__account(self):
        self.assertEquals("person_one", str(self.account_one))

    def test__str__transaction(self):
        transaction = Transaction(payer_account=self.account_one,
                                  payee_account=self.account_two,
                                  amount=200,
                                  description='test transaction'
                                  )
        self.assertEquals("person_one paid to person_two 200. Remarks: test transaction",
                          str(transaction))

    def test__str__transaction_without_description(self):
        transaction = Transaction(payer_account=self.account_one,
                                  payee_account=self.account_two,
                                  amount=1)
        self.assertEquals("person_one paid to person_two 1.", str(transaction))

    def test_transaction_with_all_validations(self):
        transaction = Transaction(payer_account=self.account_one,
                                  payee_account=self.account_two,
                                  amount=1)
        transaction.clean()
        self.assertEquals("person_one paid to person_two 1.", str(transaction))

    def test_payer_payee_same_in_transaction(self):
        invalid_transaction = Transaction(payer_account=self.account_one,
                                          payee_account=self.account_one,
                                          amount=1000,
                                          description='payer is same as payee, transaction should not be created'
                                          )

        with self.assertRaises(ValidationError) as validation_error:
            invalid_transaction.clean()

        self.assertEquals(validation_error.exception.messages,
                          [u'Payer and payee account must not be same'])

    def test_transaction_amount_more_than_payer_account_balance(self):
        invalid_transaction = Transaction(payer_account=self.account_one,
                                          payee_account=self.account_two,
                                          amount=1600,
                                          description='Transaction amount is more than payer account balance'
                                          )

        with self.assertRaises(ValidationError) as validation_error:
            invalid_transaction.clean()

        self.assertEquals(validation_error.exception.messages,
                          [u'Payer account balance is not sufficient to complete this transaction, short by 100'])

    def test_transaction_amount_zero(self):
        zero_amount_transaction = Transaction(payer_account=self.account_one,
                                              payee_account=self.account_two,
                                              amount=0,
                                              description='Zero amount transaction')
        with self.assertRaises(ValidationError) as validation_error:
            zero_amount_transaction.clean()

        self.assertEquals(validation_error.exception.messages,
                          ['Transaction amount can not be zero'])