# -*- coding: utf-8 -*-
from django.test import TestCase

from banker.forms import GameForm


class TestGameForm(TestCase):
    fixtures = ['test-data.json']

    def test_create_new_game_form(self):
        new_game_form = GameForm()

        players_eligible_for_game = list()
        for choice in new_game_form.fields['players'].queryset:
            players_eligible_for_game.append(choice)

        self.assertEquals(3, len(players_eligible_for_game), "No of entries in the game form must be 3, but was %d" %
                          len(players_eligible_for_game))
