# -*- coding: utf-8 -*-
# topmanagerbot/items.py

from scrapy import Item, Field


class CountryItem(Item):
    flag_slug = Field()
    name = Field()
    tm_id = Field()


class LeagueItem(Item):
    country = Field()
    logo_slug = Field()
    name = Field()
    tm_id = Field()
    tm_slug = Field()


class ClubItem(Item):
    country = Field()
    league = Field()
    logo_slug = Field()
    name = Field()
    seats_number = Field()
    stadium = Field()
    tm_id = Field()
    tm_slug = Field()


class FootballerItem(Item):
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
