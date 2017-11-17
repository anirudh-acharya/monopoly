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
        return Game.objects.all()


class GameDetail(View):
    form_class = TransactionForm
    template_name = 'banker/game.html'


    def get(self, request, game_id):
        from banker.models import Game
        game = get_object_or_404(Game, id=game_id)
        game_accounts = game.account_set.all()

        form = TransactionForm(game_id=game_id)

        recent_transactions = Transaction.objects.filter(
                payer_account__game_id=game_id,
                payee_account__game_id=game_id).order_by("-id")[:10]

        context = {'game_accounts': game_accounts,
            'form': form,
            'recent_transactions': recent_transactions}

        return render(request, 'banker/game.html', context)


    def post(self, request, game_id):
        form = TransactionForm(request.POST, game_id=game_id)
        if form.is_valid():
            transaction = form.save()

        return redirect('game', game_id)
