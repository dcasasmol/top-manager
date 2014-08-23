# -*- coding: utf-8 -*-
# topmanagerbot/pipelines.py

import urllib

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline

from api.models import Country, League, Club, Injury, Footballer, \
    Nationality, PlayingPosition, Position
from .settings import DEFAULT_NA, DJANGO_PROJECT_PATH
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

        if item[u'injury_info']:
            spider.counters[u'injuried_players'] += 1

        if item[u'new_arrival_from']:
            spider.counters[u'new_arrivals'] += 1

        if item[u'new_arrival_price'] == u'loan':
            spider.counters[u'loans'] += 1

        # return item

    def process_country(self, item, spider):

        spider.counters[u'countries_processed'] += 1

        try:

            country = Country.objects.get(tm_id=item[u'tm_id'])

        except Country.DoesNotExist:

            country = CountryItem(dict(item))

        # return item

    def process_club(self, item, spider):
        spider.counters[u'clubs_processed'] += 1
        # return item

    def process_league(self, item, spider):
        spider.counters[u'leagues_processed'] += 1
        # return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.clubs_seen = set()
        self.countries_seen = set()
        self.footballers_seen = set()
        self.leagues_seen = set()

    def process_item(self, item, spider):

        if item[u'name'] == DEFAULT_NA:
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
