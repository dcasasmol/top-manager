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
            footballer[u'height'] = self.parse_height(item[u'height'])
            footballer[u'number'] = item[u'number'] if item[u'number'] else u''

            if item[u'foot']:
                footballer[u'foot'] = self.parse_foot(item[u'foot'])

            # Sets footballer club object.
            footballer[u'club'] = self.get_club_object(item[u'club'])

            # Sets new arrival info if exists.
            if item[u'new_arrival_from']:
                footballer[u'new_arrival_from'] = self.get_club_object(item[u'new_arrival_from'])
                spider.counters[u'new_arrivals'] += 1

                if item[u'new_arrival_price'] == u'loan':
                    footballer[u'new_arrival_price'] = 0
                    spider.counters[u'loans'] += 1

                elif item[u'new_arrival_price']:
                    footballer[u'new_arrival_price'] = int(item[u'new_arrival_price'])

                else:
                    footballer[u'new_arrival_price'] = None

            else:
                footballer[u'new_arrival_from'] = None
                footballer[u'new_arrival_price'] = None

            # Saves footballer injury if exists.
            if item[u'injury_info']:
                injury = Injury(name=footballer[u'name'])
                injury.description = item[u'injury_info']
                injury.duration = self.get_injury_duration(item[u'injury_return'])
                injury.save()

                footballer[u'injury'] = injury
                spider.counters[u'injuried_players'] += 1

            footballer.save()
            footballer = self.get_footballer_object(footballer[u'tm_id'])
            spider.counters[u'footballers_saved'] += 1

            # Saves footballer nationalities.
            primary = True
            for one_country in item[u'countries']:
                country = self.get_country_object(one_country)

                nationality = Nationality(name=u'%s - %s' % (footballer.name,
                                                             country.name))
                nationality.country = country
                nationality.footballer = footballer

                if primary:
                    nationality.primary = primary
                    primary = False

                nationality.save()

            # Saves footballer playing positions.
            for one_position in item[u'main_position']:
                position = self.get_position_object(one_position)

                playing_position = PlayingPosition(name=u'%s - %s' % (footballer.name,
                                                                      position.name))
                playing_position.position = position
                playing_position.footballer = footballer
                playing_position.primary = True
                playing_position.save()

            for one_position in item[u'secondary_positions']:
                position = self.get_position_object(one_position)

                playing_position = PlayingPosition(name=u'%s - %s' % (footballer.name,
                                                                      position.name))
                playing_position.position = position
                playing_position.footballer = footballer
                playing_position.save()

        return item

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

            country.save()
            spider.counters[u'countries_saved'] += 1

        return item

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
            club.save()
            spider.counters[u'clubs_saved'] += 1

        return item

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
            league.save()
            spider.counters[u'leagues_saved'] += 1

        return item

    def get_club_object(self, club_id):

        return Club.objects.filter(tm_id=club_id).first()

    def get_country_object(self, country_id):

        return Country.objects.filter(tm_id=country_id).first()

    def get_footballer_object(self, footballer_id):

        return Footballer.objects.filter(tm_id=footballer_id).first()

    def get_league_object(self, league_id):

        return League.objects.filter(tm_id=league_id).first()

    def get_position_object(self, position_name):

        if position_name == u'Keeper':
            position_name = u'Goalkeeper'

        return Position.objects.filter(name=position_name.replace(u'-', u' ')).first()

    def get_injury_duration(self, return_str):

        duration = None
        return_date = self.parse_date(return_str)

        if return_date:
            # Gets the next weekend of the return date.
            while return_date.weekday() != 5:
                return_date += datetime.timedelta(days=1)

            timedelta = return_date - datetime.date.today()
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

    def parse_foot(self, string):

        if string.lower() == Footballer.RIGHT_HANDED:
            foot = Footballer.RIGHT_HANDED
        elif string.lower() == Footballer.LEFT_HANDED:
            foot = Footballer.LEFT_HANDED
        elif string.lower() == Footballer.AMBIDEXTROUS:
            foot = Footballer.AMBIDEXTROUS
        else:
            foot = None

        return foot

    def parse_height(self, string):

        return float(string.replace(u',', u'.').split(u' ')[0]) if string else None


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
