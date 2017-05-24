#!/usr/bin/python

from django.test import TestCase
from banker.models import Game, Player, Account, Transaction

from banker import signals


class SignalTestCases(TestCase):
    def setUp(self):
        game = Game.objects.create()

        player_one = Player.objects.create(person_id=1)
        player_two = Player.objects.create(person_id=2)

        account_one = Account.objects.create(game=game,
                player=player_one,
                balance=1500)

        account_two = Account.objects.create(game=game,
                player=player_two,
                balance=1500)

        transaction = Transaction.objects.create(payer_account=player_one,
                payee_account=player_two,
                amount = 200,
                description = 'test transaction'
                )

    def test_update_account_balance(self):
        update_accout_balance(Transaction.__class__,
                instance=transaction,
                create=True,
                raw=False,
                using='default',
                update_fields=None
                )

