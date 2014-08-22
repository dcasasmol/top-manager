# -*- coding: utf-8 -*-
# api/urls.py

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',

    url(r'countries^$',
        views.CountryList.as_view(),
        name='countries-list'),

    url(r'^countries/new$',
        views.CountryCreate.as_view(),
        name='country-new'),

    url(r'^countries/edit/(?P<pk>\d+)$',
        views.CountryUpdate.as_view(),
        name='country-edit'),

    url(r'^countries/delete/(?P<pk>\d+)$',
        views.CountryDelete.as_view(),
        name='country-delete'),
)
