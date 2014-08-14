# -*- coding: utf-8 -*-
# topmanagerbot/pipelines.py

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from topmanagerbot.items import CountryItem, LeagueItem


class TopmanagerbotPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, CountryItem):
            return self.storeCountry(item, spider)

        elif isinstance(item, LeagueItem):
            return self.storeLeague(item, spider)


    def storeCountry(self, item, spider):

        return item


    def storeLeague(self, item, spider):

        return item
