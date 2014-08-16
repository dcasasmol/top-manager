# -*- coding: utf-8 -*-
# topmanagerbot/pipelines.py

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from topmanagerbot import items


class TopmanagerbotPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, items.Footballer):
            return self.storeFootballer(item, spider)

        elif isinstance(item, items.Country):
            return self.storeCountry(item, spider)

        elif isinstance(item, items.Club):
            return self.storeClub(item, spider)

        elif isinstance(item, items.League):
            return self.storeLeague(item, spider)


    def storeFootballer(self, item, spider):
        spider.counters['footballers_processed'] += 1
        return item

    def storeCountry(self, item, spider):
        spider.counters['countries_processed'] += 1
        return item

    def storeClub(self, item, spider):
        spider.counters['clubs_processed'] += 1
        return item

    def storeLeague(self, item, spider):
        spider.counters['leagues_processed'] += 1
        return item
