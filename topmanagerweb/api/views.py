# -*- coding: utf-8 -*-
# api/views.py

from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Country, Position, League, Club, Injury, Footballer, \
    Nationality, PlayingPosition


class CountryList(ListView):
    model = Country


class CountryCreate(CreateView):
    model = Country
    success_url = reverse_lazy('countries-list')


class CountryUpdate(UpdateView):
    model = Country
    success_url = reverse_lazy('countries-list')


class CountryDelete(Delete):
    model = Country
    success_url = reverse_lazy('countries-list')
