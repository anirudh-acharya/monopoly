from django.conf.urls import url

from banker.constants.view_names import GAME_DETAIL_VIEW_NAME, INDEX_VIEW_NAME, NEW_GAME_VIEW_NAME
from banker.views import IndexView, GameDetailView, NewGameView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name=INDEX_VIEW_NAME),
    url(r'^newgame$', NewGameView.as_view(), name=NEW_GAME_VIEW_NAME),
    url(r'^(?P<game_id>[0-9]+)/$', GameDetailView.as_view(), name=GAME_DETAIL_VIEW_NAME),
]
