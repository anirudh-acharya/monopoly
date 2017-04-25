# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Game,Player,Account,Transaction


admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Account)
admin.site.register(Transaction)
