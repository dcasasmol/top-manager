# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.contrib.djangoitem import DjangoItem
from scrapy.item import Field


class PlayerItem(DjangoItem):
    # Fields for this item are automatically created from the Django model
    django_model = Player
