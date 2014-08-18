# -*- coding: utf-8 -*-
# topmanagerbot/pipelines.py

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

from .items import ClubItem, CountryItem, FootballerItem, LeagueItem
from .settings import DEFAULT_NA


class ProcessPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, FootballerItem):

            if item[u'injury_info']:
                spider.counters[u'injuried_players'] += 1

            if item[u'new_arrival_from']:
                spider.counters[u'new_arrivals'] += 1

            if item[u'new_arrival_amount'] == 'loan':
                spider.counters[u'loans'] += 1

            return self.store_footballer(item, spider)

        elif isinstance(item, CountryItem):
            return self.store_country(item, spider)

        elif isinstance(item, ClubItem):
            return self.store_club(item, spider)

        elif isinstance(item, LeagueItem):
            return self.store_league(item, spider)

    def store_footballer(self, item, spider):
        spider.counters[u'footballers_processed'] += 1
        return item

    def store_country(self, item, spider):
        spider.counters[u'countries_processed'] += 1
        return item

    def store_club(self, item, spider):
        spider.counters[u'clubs_processed'] += 1
        return item

    def store_league(self, item, spider):
        spider.counters[u'leagues_processed'] += 1
        return item


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
