# -*- coding: utf-8 -*-
# api/admin.py

from django.contrib import admin
from .models import Country, Position, League, Club, Injury, Footballer, \
    Nationality, PlayingPosition

admin.site.register(Country)
admin.site.register(Position)
admin.site.register(League)
admin.site.register(Club)
admin.site.register(Footballer)
admin.site.register(Injury)
admin.site.register(Nationality)
admin.site.register(PlayingPosition)

