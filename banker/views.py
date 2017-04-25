# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


def index(request):
    """
    """
    from .models import Game
    games = Game.objects.all()
    context = {'games': games}
    return render(request, 'banker/index.html', context)


def detail(request, game_id):
    """
    """
    from .models import Game
    game = get_object_or_404(Game, id=game_id)
    game_accounts = game.account_set.all()

    context = {'game_accounts': game_accounts}
    return render(request, 'banker/detail.html', context)
