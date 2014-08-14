# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# from scrapy.contrib.djangoitem import DjangoItem
from scrapy import Item, Field

# from api.models import Country, League, Club, Footballer

# class FootballerItem(DjangoItem):
#     # Fields for this item are automatically created from the Django model
#     django_model = Footballer

class CountryItem(Item):
    name = Field()
    flag_slug = Field()


class LeagueItem(Item):
    name = Field()
    transfermarkt_slug = Field()
    logo_slug = Field()
    country = Field()

