# -*- coding: utf-8 -*-
# topmanagerbot/pipelines.py

import math
import urllib
import datetime

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline

from api.models import Country, League, Club, Injury, Footballer, \
    Nationality, PlayingPosition, Position
from .settings import DJANGO_PROJECT_PATH
from .items import ClubItem, CountryItem, FootballerItem, LeagueItem, \
    NationalityItem, PlayingPositionItem


class ProcessPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, FootballerItem):
            return self.process_footballer(item, spider)

        elif isinstance(item, CountryItem):
            return self.process_country(item, spider)

        elif isinstance(item, ClubItem):
            return self.process_club(item, spider)

        elif isinstance(item, LeagueItem):
            return self.process_league(item, spider)

    def process_footballer(self, item, spider):
        spider.counters[u'footballers_processed'] += 1

        if item[u'new_arrival_from']:
            spider.counters[u'new_arrivals'] += 1

        if item[u'new_arrival_price'] == u'loan':
            spider.counters[u'loans'] += 1

        try:
            footballer = Footballer.objects.get(tm_id=item[u'tm_id'])

        except Footballer.DoesNotExist:
            footballer = FootballerItem(dict(item))

            # Sets footballer photo.
            if item[u'images']:
                footballer[u'photo'] = item[u'images'][0][u'path']
            else:
                footballer[u'photo'] = u''

            # Processes footballer fields.
            footballer[u'arrived_date'] = self.parse_date(item[u'arrived_date'])
            footballer[u'birth_date'] = self.parse_date(item[u'birth_date'])
            footballer[u'contract_until'] = self.parse_date(item[u'contract_until'])
            # footballer[u'height'] # TODO to float
            # footballer[u'foot'] # TODO to Footballer.FOOT_CHOICES
            # footballer[u'new_arrival_from'] # TODO to Club
            # footballer[u'new_arrival_price'] # TODO to int
            # footballer[u'number'] # TODO to str (None if u'')

            # Sets footballer club object.
            footballer[u'club'] = self.get_club_object(item[u'club'])

            # Saves footballer nationalities.
            # TODO

            # Saves footballer playing positions.
            # TODO

            # Saves footballer injury if exists.
            if item[u'injury_info']:
                injury = Injury(name=footballer[u'name'])
                injury.description = item[u'injury_info']
                injury.duration = self.get_injury_duration(item[u'injury_return'])

                spider.counters[u'injuried_players'] += 1

        print("============")
        print("============")
        print("============")
        print(footballer)
        print("============")
        print("============")
        print("============")
        # return item

    def process_country(self, item, spider):

        spider.counters[u'countries_processed'] += 1

        try:
            country = Country.objects.get(tm_id=item[u'tm_id'])

        except Country.DoesNotExist:
            country = CountryItem(dict(item))

            # Sets country flag.
            if item[u'images']:
                country[u'flag'] = item[u'images'][0][u'path']
            else:
                country[u'flag'] = u''

        # return item

    def process_club(self, item, spider):
        spider.counters[u'clubs_processed'] += 1

        try:
            club = Club.objects.get(tm_id=item[u'tm_id'])

        except Club.DoesNotExist:

            club = ClubItem(dict(item))

            # Sets club crest.
            if item[u'images']:
                club[u'crest'] = item[u'images'][0][u'path']
            else:
                club[u'crest'] = u''

            # Sets club league and country objects.
            club[u'country'] = self.get_country_object(item[u'country'])
            club[u'league'] = self.get_league_object(item[u'league'])

        # return item

    def process_league(self, item, spider):
        spider.counters[u'leagues_processed'] += 1

        try:
            league = League.objects.get(tm_id=item[u'tm_id'])

        except League.DoesNotExist:

            league = LeagueItem(dict(item))

            # Sets league logo.
            if item[u'images']:
                league[u'logo'] = item[u'images'][0][u'path']
            else:
                league[u'logo'] = u''

            # Sets league country object.
            league[u'country'] = self.get_country_object(item[u'country'])

        # return item

    def get_country_object(self, country_id):
        return Country.objects.filter(tm_id=country_id).first()

    def get_league_object(self, league_id):
        return League.objects.filter(tm_id=league_id).first()

    def get_club_object(self, club_id):
        return Club.objects.filter(tm_id=club_id).first()

    def get_position_object(self, position_name):
        return Position.objects.filter(name=position_name).first()

    def get_injury_duration(self, return_str):
        duration = None
        return_date = self.parse_date(return_str)

        if return_date:
            # Gets the next weekend of the return date.
            while return_date.weekday() != 5:
                return_date += datetime.timedelta(days=1)

            today = datetime.datetime.today().date()
            timedelta = return_date - today
            duration = int(math.floor(timedelta.days / 7.0))

        return duration

    def parse_date(self, string):
        if u'.' in string:
            date = datetime.datetime.strptime(string, u'%d.%m.%Y').date()
        elif u',' in string:
            date = datetime.datetime.strptime(string, u'%b %d, %Y').date()
        else:
            date = None

        return date


class DuplicatesPipeline(object):

    def __init__(self):
        self.clubs_seen = set()
        self.countries_seen = set()
        self.footballers_seen = set()
        self.leagues_seen = set()

    def process_item(self, item, spider):

        if not item[u'name']:
            raise DropItem(u'Empty item found: %s' % item)

        if isinstance(item, FootballerItem):
            return self.check_footballer_duplicated(item, spider)

        elif isinstance(item, CountryItem):
            return self.check_country_duplicated(item, spider)

        elif isinstance(item, ClubItem):
            return self.check_club_duplicated(item, spider)

        elif isinstance(item, LeagueItem):
            return self.check_league_duplicated(item, spider)

    def check_league_duplicated(self, item, spider):

        if item[u'tm_id'] in self.leagues_seen:
            spider.counters[u'leagues_duplicated'] += 1
            raise DropItem(u'uplicate league found: %s' % item)
        else:
            self.leagues_seen.add(item[u'tm_id'])
            return item

    def check_club_duplicated(self, item, spider):

        if item[u'tm_id'] in self.clubs_seen:
            spider.counters[u'clubs_duplicated'] += 1
            raise DropItem(u'Duplicate club found: %s' % item)
        else:
            self.clubs_seen.add(item[u'tm_id'])
            return item

    def check_footballer_duplicated(self, item, spider):

        if item[u'tm_id'] in self.footballers_seen:
            spider.counters[u'footballers_duplicated'] += 1
            raise DropItem(u'Duplicate footballer found: %s' % item)
        else:
            self.footballers_seen.add(item[u'tm_id'])
            return item

    def check_country_duplicated(self, item, spider):

        if item[u'tm_id'] in self.countries_seen:
            spider.counters[u'countries_duplicated'] += 1
            raise DropItem(u'Duplicate country found: %s' % item)
        else:
            self.countries_seen.add(item[u'tm_id'])
            return item


class SaveImagesPipeline(ImagesPipeline):

    def image_key(self, url):

        # Sets the filename of the downloaded files.
        filename = url.split(u'/')[-1]
        name = filename.split(u'.')[0]

        slug = self.get_slug(url)

        if slug == u'footballers/':
            if u'-' in name:
                name = name.split(u'-')[0]
            elif u'_' in name:
                name = name.split(u'_')[1]

        return u'%s%s.jpg' % (slug, name)

    def thumb_key(self, url, thumb_id):

        # Sets the filename of the downloaded thumbnail files.
        filename = url.split(u'/')[-1]
        name = filename.split(u'.')[0]

        slug = self.get_slug(url)

        if slug == u'footballers/':
            if u'-' in name:
                name = name.split(u'-')[0]
            elif u'_' in name:
                name = name.split(u'_')[1]

        return u'%sthumb-%s-%s.jpg' % (slug, thumb_id, name)

    def get_slug(self, url):

      if u'spieler' in url:
          slug = u'footballers/'
      elif u'flagge' in url:
          slug = u'flags/'
      elif u'wappen' in url:
          slug = u'clubs/'
      elif u'logo' in url:
          slug = u'leagues/'
      else:
          slug = u'footballers/'

      return slug
