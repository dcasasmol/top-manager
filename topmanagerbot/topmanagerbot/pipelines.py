# -*- coding: utf-8 -*-
# topmanagerbot/pipelines.py

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

from topmanagerbot import items


class ProcessPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, items.Footballer):
            return self.store_footballer(item, spider)

        elif isinstance(item, items.Country):
            return self.store_country(item, spider)

        elif isinstance(item, items.Club):
            return self.store_club(item, spider)

        elif isinstance(item, items.League):
            return self.store_league(item, spider)

    def store_footballer(self, item, spider):
        spider.counters['footballers_processed'] += 1
        return item

    def store_country(self, item, spider):
        spider.counters['countries_processed'] += 1
        return item

    def store_club(self, item, spider):
        spider.counters['clubs_processed'] += 1
        return item

    def store_league(self, item, spider):
        spider.counters['leagues_processed'] += 1
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.clubs_seen = set()
        self.countries_seen = set()
        self.footballers_seen = set()
        self.leagues_seen = set()

    def process_item(self, item, spider):

        if item['name'] == 'N/A':
            raise DropItem("Empty item found: %s" % item)

        if isinstance(item, items.Footballer):
            return self.check_footballer_duplicated(item, spider)

        elif isinstance(item, items.Country):
            return self.check_country_duplicated(item, spider)

        elif isinstance(item, items.Club):
            return self.check_club_duplicated(item, spider)

        elif isinstance(item, items.League):
            return self.check_league_duplicated(item, spider)

    def check_league_duplicated(self, item, spider):

        if item['tm_id'] in self.leagues_seen:
            spider.counters['leagues_duplicated'] += 1
            raise DropItem("Duplicate league found: %s" % item)
        else:
            self.leagues_seen.add(item['tm_id'])
            return item

    def check_club_duplicated(self, item, spider):

        if item['tm_id'] in self.clubs_seen:
            spider.counters['clubs_duplicated'] += 1
            raise DropItem("Duplicate club found: %s" % item)
        else:
            self.clubs_seen.add(item['tm_id'])
            return item

    def check_footballer_duplicated(self, item, spider):

        if item['tm_id'] in self.footballers_seen:
            spider.counters['footballers_duplicated'] += 1
            raise DropItem("Duplicate footballer found: %s" % item)
        else:
            self.footballers_seen.add(item['tm_id'])
            return item

    def check_country_duplicated(self, item, spider):

        if item['tm_id'] in self.countries_seen:
            spider.counters['countries_duplicated'] += 1
            raise DropItem("Duplicate country found: %s" % item)
        else:
            self.countries_seen.add(item['tm_id'])
            return item
