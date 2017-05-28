from django.conf.urls import url
from . import views
from banker.views import IndexView, GameDetail

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<game_id>[0-9]+)/$', GameDetail.as_view(), name='game'),
    ] 
