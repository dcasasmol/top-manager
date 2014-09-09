# -*- coding: utf-8 -*-
# api/views.py

from django.db.models import Max
from django.views.generic import ListView

from api.models import Footballer


class FootballerTableView(ListView):
    template_name = 'footballers-list.html'
    model = Footballer
    context_object_name = 'footballers'
    paginate_by = 10


    def get_queryset(self):
        return Footballer.objects.filter(is_active=True)
        # return sorted(Footballer.objects.filter(is_active=True),
        #               key=lambda f: f.main_position.id)

