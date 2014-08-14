# -*- coding: utf-8 -*-
# topmanagerbot/spiders/transfermarkt.py

import os
import scrapy

from topmanagerbot import settings
from topmanagerbot import items


class TransfermarktSpider(scrapy.Spider):

    name = u'transfermarkt'
    allowed_domains = [ settings.TM_HOST_NAME ]
    start_urls = ()


    def __init__(self):

        for one_league in settings.TM_LEAGUES:

            league_url = self.build_transfermarkt_url(one_league)
            self.start_urls = self.start_urls + ( league_url, )

        super(TransfermarktSpider, self).__init__()


    def parse(self, response):

        # Gets country info.
        country = items.Country(self.get_country_info(response))
        yield country

        # Gets league info.
        league = items.League(self.get_league_info(response))
        league['country'] = country['name']
        yield league

        # Gets clubs links and proccess them.
        clubs_links = self.get_clubs_links(response)
        for one_club in clubs_links:

          club_url = self.build_transfermarkt_url(one_club)
          yield scrapy.Request(url=club_url, callback=self.parse_club)


    def parse_club(self, response):
        pass


    ###############################################
    ## Functions which build dicts to create items.
    ###############################################
    def get_country_info(self, response):

        selector = scrapy.selector.Selector(response)

        country = {
            u'name': self.get_country_name(selector),
            u'flag_slug': self.get_country_flag(selector),
        }

        return country


    def get_league_info(self, response):

        selector = scrapy.selector.Selector(response)

        league = {
            u'name': self.get_league_name(selector),
            u'transfermarkt_slug': self.get_league_transfermartk_slug(response),
            u'logo_slug': self.get_league_logo_slug(selector),
            u'country': u'', # Country is setted in parse function.
        }

        return league


    ################################
    ## Utils to gets the items info.
    ################################

    def build_transfermarkt_url(self, slug):

        hosted_url = u'%s/%s' % (settings.TM_HOST_NAME, slug)
        normalized_url = u'http://www.%s' % os.path.normpath(hosted_url)

        return normalized_url


    def clean_string(self, string):

        clean_string = string

        characters = [u'\t', u'\n', u'  ']
        for one_character in characters:
            clean_string = clean_string.replace(one_character, u'')

        characters_protected = [u'\'', u'"']
        for one_protected in characters_protected:
            clean_string = clean_string.replace(one_protected, u'\\%s' % one_protected)

        return clean_string


    def get_country_name(self, selector):

        name = selector.xpath('//div[@class="flagge"]/a/img/@title').extract()

        return self.clean_string(name[0]) if name else settings.DEFAULT_NA


    def get_country_flag(self, selector):

        flag = selector.xpath('//div[@class="flagge"]/a/img/@src').extract()

        return self.clean_string(flag[0]) if flag else settings.DEFAULT_NA


    def get_league_logo_slug(self, selector):

        logo = selector.xpath('//div[@class="headerfoto"]/img/@src').extract()

        return self.clean_string(logo[0]) if logo else settings.DEFAULT_NA


    def get_league_name(self, selector):

        name = selector.xpath('//div[@class="spielername-profil"]/text()').extract()

        return self.clean_string(name[0]) if name else settings.DEFAULT_NA


    def get_league_transfermartk_slug(self, response):

        url = response.url

        return url.split(settings.TM_HOST_NAME)[-1] if url else settings.DEFAULT_NA


    def get_clubs_links(self, response):

        clubs = []
        selector = scrapy.selector.Selector(response)

        table = selector.xpath(u'//div[@id="yw1"]/table/tbody/tr')
        for one_row in table:

            td_element = one_row.xpath('.//td')

            if td_element:
                team_link = td_element[0].xpath('.//a/@href').extract()

                if team_link:
                    clubs.extend(team_link)

        return clubs
