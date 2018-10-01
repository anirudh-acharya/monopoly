# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views import generic, View
from banker.forms import TransactionForm
from banker.models import Transaction


class IndexView(generic.ListView):

    template_name = 'banker/index.html'
    context_object_name = 'games'

    def get_queryset(self):
        from banker.models import Game
        return Game.objects.all().order_by("-id")


class GameDetail(View):
    form_class = TransactionForm
    template_name = 'banker/game.html'


    def get(self, request, game_id):
        return render(request, self.template_name, self.get_game_context(game_id))


    def post(self, request, game_id):
        form = TransactionForm(game_id, request.POST)
        if form.is_valid():
            transaction = form.save()
            return redirect('game', game_id)
        else:
            return render(request, self.template_name, self.get_game_context(game_id, form))


    def get_game_context(self, game_id, form=None):
        return {
            'game_accounts': self.get_game_accounts(game_id),
            'form': form if form else TransactionForm(game_id),
            'recent_transactions': self.get_recent_transactions(game_id),}


    # TODO: Memoize
    def get_game_accounts(self, game_id):
        from banker.models import Game
        game = get_object_or_404(Game, id=game_id)
        return game.account_set.all()


    # TODO: Reduce the db calls?
    def get_recent_transactions(self, game_id):
        return Transaction.objects.filter(
                payer_account__game_id=game_id,
                payee_account__game_id=game_id).order_by("-id")[:10]

