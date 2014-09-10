# -*- coding: utf-8 -*-
# api/urls.py

from django.conf.urls import patterns, url
from .views import FootballerTableView


urlpatterns = patterns('',
    # Searcher lists footballers by default.
    url(r'^$', FootballerTableView.as_view(), name='searcher'),
    # Search leagues.
    url(r'^leagues$', FootballerTableView.as_view(), name='leagues-list'),
    # Search clubs.
    url(r'^clubs$', FootballerTableView.as_view(), name='clubs-list'),
    # Search footballers.
    url(r'^footballers$', FootballerTableView.as_view(), name='footballers-list'),
)
