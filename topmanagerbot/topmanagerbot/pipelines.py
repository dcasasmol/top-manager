# -*- coding: utf-8 -*-
# topmanagerbot/pipelines.py

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from topmanagerbot import items


class TopmanagerbotPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, Footballer):
            return self.storeFootballer(item, spider)

        elif isinstance(item, Country):
            return self.storeCountry(item, spider)

        elif isinstance(item, Club):
            return self.storeClub(item, spider)

        elif isinstance(item, League):
            return self.storeLeague(item, spider)


    def storeClub(self, item, spider):
        return item

    def storeCountry(self, item, spider):
        return item

    def storeFootballer(self, item, spider):
        return item

    def storeLeague(self, item, spider):
        return item
