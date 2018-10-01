from django.test import TestCase
from django.contrib.auth.models import User
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

        self.transaction = Transaction.objects.create(payer_account=self.account_one,
                payee_account=self.account_two,
                amount = 200,
                description = 'test transaction'
                )

    def test__str__game(self):
        game_time_created = self.game.start_time
        self.assertEquals("Game: 1", str(self.game))

    def test__str__player(self):
        self.assertEquals("person_one", str(self.player_one))

    def test__str__account(self):
        self.assertEquals("person_one", str(self.account_one))

    def test__str__transaction(self):
        self.assertEquals("person_one paid to person_two 200. Remarks: test transaction",
                str(self.transaction))

    def test__str__transaction_without_description(self):
        transaction = Transaction.objects.create(payer_account=self.account_one,
                                                 payee_account=self.account_two,
                                                 amount=1)
        self.assertEquals("person_one paid to person_two 1.", str(transaction))