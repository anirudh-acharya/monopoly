#!/usr/bin/python

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
                amount = 200,
                description = 'test transaction'
                )

        self.assertEquals(self.account_one.balance, 1300)
        self.assertEquals(self.account_two.balance, 1700)

    def test_update_account_balance_signal_for_transaction_update(self):
        self.transaction = Transaction.objects.create(payer_account=self.account_one,
                payee_account=self.account_two,
                amount = 200,
                description = 'test transaction'
                )

        self.transaction.amount = 100
        self.transaction.save()

        self.assertEquals(self.account_one.balance, 1200)
        self.assertEquals(self.account_two.balance, 1800)

    def test_payer_payee_same_in_transaction(self):
        invalid_transaction = Transaction.objects.create(payer_account=self.account_one,
                payee_account=self.account_one,
                amount=1000,
                description='payer is same as payee, transaction should not be created'
                )

        with self.assertRaises(ValidationError) as validation_error:
            invalid_transaction.full_clean()

        self.assertEquals(validation_error.exception.messages,
                [u'Payer and payee account must not be same'])

    def test_transaction_amount_more_than_payer_account_balance(self):
        # full_clean method for validation doesn't run on save automatically
        # To verify the functionality, Keeping the amount as 800,
        # So after this transaction is created, account balance becomes 1500 - 800 = 700
        # And post which when the validation occurs, the error thrown shows the amount
        # as 100 rupee lesser
        invalid_transaction = Transaction.objects.create(payer_account=self.account_one,
                payee_account=self.account_two,
                amount=800,
                description='Transaction amount is more than payer account balance'
                )

        with self.assertRaises(ValidationError) as validation_error:
            invalid_transaction.full_clean()

        self.assertEquals(validation_error.exception.messages,
                [u'Payer account balance is not sufficient to complete this transaction, short by 100'])
