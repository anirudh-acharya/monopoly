# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test.client import Client
from django.test import TestCase
from django.urls import reverse

from banker.constants.view_names import INDEX_VIEW_NAME, NEW_GAME_VIEW_NAME, GAME_DETAIL_VIEW_NAME
from banker.models import Game
from banker.views import NewGameView


class ViewsTestCases(TestCase):
    fixtures = ['test-data.json']

    def test_get_index(self):
        response = self.client.get(reverse(INDEX_VIEW_NAME))
        self.assertEquals(200, response.status_code)

    def test_get_game_detail(self):
        response = self.client.get(reverse(GAME_DETAIL_VIEW_NAME, args=u'1'))
        self.assertEquals(200, response.status_code)

    def test_new_game_get(self):
        response = self.client.get(reverse(NEW_GAME_VIEW_NAME))
        self.assertEquals(200, response.status_code)

    def test_new_game_post(self):
        last_game_before = Game.objects.last()
        response = self.client.post(reverse(NEW_GAME_VIEW_NAME), {u'players': [u'1', u'2']}, follow=True)
        last_game_after = Game.objects.last()
        self.assertGreater(last_game_after.id, last_game_before.id, "Last game id after submitting the new game for" +\
                           "must be greater than that of before submitting the form")

        num_of_accounts_in_new_game = last_game_after.account_set.count()
        self.assertEquals(3, num_of_accounts_in_new_game, "Number of accounts in the new game must be 3, " +\
                          "but was %s " % num_of_accounts_in_new_game)

        first_account = last_game_after.account_set.get(player_id=1)
        second_account = last_game_after.account_set.get(player_id=2)
        banker_account = last_game_after.account_set.get(player__person__username='bank')

        self.assertEquals(1500, first_account.balance)
        self.assertEquals(1500, second_account.balance)
        self.assertLess(1500, banker_account.balance, "Banker account balance must be greater than 1500")
        self.assertEquals('/banker/%s/' % last_game_after.id, response.redirect_chain[0][0])