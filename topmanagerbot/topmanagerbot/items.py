# -*- coding: utf-8 -*-
# topmanagerbot/items.py

from api.models import Country, League, Club, Injury, Footballer, \
    Nationality, PlayingPosition

from scrapy import Field
from scrapy.contrib.djangoitem import DjangoItem


class CountryItem(DjangoItem):
    django_model = Country

    # ImagesPipeline fields.
    image_urls = Field()
    images = Field()


class LeagueItem(DjangoItem):
    django_model = League

    # ImagesPipeline fields.
    image_urls = Field()
    images = Field()


class ClubItem(DjangoItem):
    django_model = Club

    # ImagesPipeline fields.
    image_urls = Field()
    images = Field()


class FootballerItem(DjangoItem):
    django_model = Footballer

    # ImagesPipeline fields.
    image_urls = Field()
    images = Field()

    # Django ForeignKey fields.
    countries = Field()
    injury_info = Field()
    injury_return = Field()
    main_position = Field()
    secondary_positions = Field()


class NationalityItem(DjangoItem):
    django_model = Nationality


class PlayingPositionItem(DjangoItem):
    django_model = PlayingPosition
