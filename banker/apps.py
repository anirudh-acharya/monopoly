# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class BankerConfig(AppConfig):
    name = 'banker'

    def ready(self):
        from banker import signals
