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

class Country(Item):
    flag_slug = Field()
    name = Field()
    tm_id = Field()


class League(Item):
    country = Field()
    logo_slug = Field()
    name = Field()
    tm_id = Field()
    tm_slug = Field()


class Club(Item):
    country = Field()
    league = Field()
    logo_slug = Field()
    name = Field()
    seats_number = Field()
    stadium = Field()
    tm_id = Field()
    tm_slug = Field()


class Footballer(Item):
    arrived_date = Field()
    birth_date = Field()
    birth_place = Field()
    photo_slug = Field()
    captain = Field()
    club = Field()
    contract_until = Field()
    foot = Field()
    full_name = Field()
    height = Field()
    injury_info = Field() #optional
    injury_return = Field() #optional
    main_position = Field()
    name = Field()
    nationalities = Field()
    new_arrival_from = Field() #optional
    new_arrival_amount = Field() #optional
    number = Field()
    secondary_positions = Field() #optional
    tm_id = Field()
    tm_slug = Field()
    value = Field()
