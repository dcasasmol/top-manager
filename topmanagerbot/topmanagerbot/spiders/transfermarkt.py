# -*- coding: utf-8 -*-
# topmanagerbot/spiders/transfermarkt.py

# .:: TODO list::.
# Email with report of suspicious changes.
# Save items in Django database.

import os
import scrapy

from topmanagerbot.settings import TM_HOST_NAME, TM_LEAGUES
from topmanagerbot.items import ClubItem, CountryItem, FootballerItem, LeagueItem


class TransfermarktSpider(scrapy.Spider):

    name = u'transfermarkt'
    allowed_domains = [ TM_HOST_NAME ]
    start_urls = ()
    counters = {
        u'countries_processed': 0,
        u'leagues_processed': 0,
        u'clubs_processed': 0,
        u'footballers_processed': 0,
        u'countries_duplicated': 0,
        u'leagues_duplicated': 0,
        u'clubs_duplicated': 0,
        u'footballers_duplicated': 0,
        u'injuried_players': 0,
        u'loans': 0,
        u'new_arrivals': 0,
    }


    def __init__(self):

        for one_league in TM_LEAGUES:

            league_url = self.build_tm_url(one_league)
            self.start_urls = self.start_urls + ( league_url, )

        dispatcher = scrapy.xlib.pydispatch.dispatcher
        dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)
        super(TransfermarktSpider, self).__init__()


    def parse(self, response):

        # Gets country info.
        country = CountryItem(self.get_country_info(response))

        yield country

        # Gets league info.
        league = LeagueItem(self.get_league_info(response))
        league[u'country'] = country[u'tm_id']

        yield league

        # Gets clubs links and proccess them.
        clubs_links = self.get_tm_links(response)

        meta = {
            u'league': league[u'tm_id'],
        }

        for one_club in clubs_links:

          club_url = self.build_tm_url(one_club)
          yield scrapy.Request(url=club_url, meta=meta, callback=self.parse_club)


    def parse_club(self, response):

        meta = response.meta

        # Gets country info.
        country = CountryItem(self.get_country_info(response))

        yield country

        # Gets club info.
        club = ClubItem(self.get_club_info(response))
        club[u'country'] = country[u'tm_id']
        club[u'league'] = meta.get(u'league', u'')

        yield club

        # Gets footballers links and proccess them.
        footballers_links = self.get_tm_links(response)

        meta = {
            u'club': club[u'tm_id'],
        }

        for one_footballer in footballers_links:

          if u'spieler' in one_footballer:
              footballer_url = self.build_tm_url(one_footballer)
              yield scrapy.Request(url=footballer_url, meta=meta, callback=self.parse_footballer)


    def parse_footballer(self, response):

        meta = response.meta

        # Gets nationality info.
        countries = []
        nationalities = self.get_footballer_nationalities(response)
        for one_nationality in nationalities:
            country = CountryItem(one_nationality)
            countries.append(one_nationality[u'tm_id'])

            yield country

        # Gets footballer info.
        footballer = FootballerItem(self.get_footballer_info(response))
        footballer[u'club'] = meta.get(u'club', u'')
        footballer[u'countries'] = countries

        yield footballer


    ###############################################
    ## Functions which build dicts to create items.
    ###############################################
    def get_country_info(self, response):

        selector = scrapy.selector.Selector(response)

        country = {
            u'images': [],
            u'image_urls': self.get_country_flag_url(selector),
            u'name': self.get_country_name(selector),
        }

        # Sets tm_id.
        if country[u'image_urls']:
            country[u'tm_id'] = self.get_tm_id(country[u'image_urls'][0])
        else:
            country[u'tm_id'] = u''

        return country


    def get_league_info(self, response):

        selector = scrapy.selector.Selector(response)

        league = {
            u'country': u'', # Country is setted in parse function.
            u'images': [],
            u'image_urls': self.get_tm_logo_url(selector),
            u'name': self.get_tm_name(selector),
            u'tm_slug': self.get_tm_url_slug(response),
        }

        # Sets tm_id.
        league[u'tm_id'] = self.get_tm_id(league[u'tm_slug'])

        return league


    def get_club_info(self, response):

        selector = scrapy.selector.Selector(response)

        club = {
            u'country': u'', # Country is setted in parse_club function.
            u'league': u'', # League is setted in parse_club function.
            u'images': [],
            u'image_urls': self.get_tm_logo_url(selector),
            u'name': self.get_tm_name(selector),
            u'seats': self.get_club_seats(selector),
            u'stadium': self.get_club_stadium(selector),
            u'tm_slug': self.get_tm_url_slug(response),
        }

        # Sets tm_id.
        club[u'tm_id'] = self.get_tm_id(club[u'tm_slug'])

        return club


    def get_footballer_info(self, response):

        selector = scrapy.selector.Selector(response)

        footballer = {
            u'arrived_date': self.get_footballer_personal_info(selector, u'since'),
            u'birth_date': self.get_footballer_personal_info(selector, u'Date'),
            u'birth_place': self.get_footballer_personal_info(selector, u'Place'),
            u'images': [],
            u'image_urls': self.get_tm_logo_url(selector),
            u'captain': self.get_footballer_is_captain(selector),
            u'club': u'', # Club is setted in parse_footballer function.
            u'contract_until': self.get_footballer_personal_info(selector, u'until'),
            u'foot': self.get_footballer_personal_info(selector, u'Foot'),
            u'full_name': self.get_footballer_personal_info(selector, u'ame'),
            u'height': self.get_footballer_personal_info(selector, u'Height'),
            u'main_position': self.get_footballer_position(selector, u'Main'),
            u'name': self.get_tm_name(selector),
            u'countries': u'', # Countries is setted in parse_footballer function.
            u'number': self.get_footballer_number(selector),
            u'secondary_positions': self.get_footballer_position(selector, u'Secondary'),
            u'tm_slug': self.get_tm_url_slug(response),
            u'value': self.get_footballer_value(selector),
        }

        # Sets tm_id.
        footballer[u'tm_id'] = self.get_tm_id(footballer[u'tm_slug'])

        # If does not have full_name, sets name as full_name.
        if not footballer[u'full_name']:
            footballer[u'full_name'] = footballer[u'name']

        # Sets arrival info.
        new_arrival = self.get_footballer_is_arrived(selector)
        footballer[u'new_arrival_from'] = new_arrival[u'from_team']
        footballer[u'new_arrival_price'] = new_arrival[u'amount']

        # Sets injury info.
        injury = self.get_footballer_injury(selector)
        footballer[u'injury_info'] = injury[u'info']
        footballer[u'injury_return'] = injury[u'return']

        return footballer


    ################################
    ## Utils to gets the items info.
    ################################

    def build_tm_url(self, slug):

        hosted_url = u'%s/%s' % (TM_HOST_NAME, slug)
        normalized_url = u'http://www.%s' % os.path.normpath(hosted_url)

        return normalized_url


    def clean_string(self, string):

        clean_string = string

        characters = [u'\r', u'\t', u'\n', u'  ', u'\xa0']
        for one_character in characters:
            clean_string = clean_string.replace(one_character, u'')

        characters_protected = [u'\'', u'"']
        for one_protected in characters_protected:
            clean_string = clean_string.replace(one_protected, u'\\%s' % one_protected)

        return clean_string


    def get_club_seats(self, selector):

        seats = selector.xpath(u'//table[@class="profilheader"]/tr/td/span[contains(text(), "Seats")]/text()').extract()

        if seats:
          seats_number = seats[0].split(u' ')[0]
        else:
          seats_number = u''

        return int(seats_number.replace(u'.', u'')) if seats_number else 0


    def get_club_stadium(self, selector):

        stadium = selector.xpath(u'//table[@class="profilheader"]/tr/td/a[contains(@href, "stadion")]/text()').extract()

        return self.clean_string(stadium[0]) if stadium else u''


    def get_country_name(self, selector):

        name = selector.xpath(u'//div[@class="flagge"]/a/img/@title').extract()

        return self.clean_string(name[0]) if name else u''


    def get_country_flag_url(self, selector):

        flag_info = selector.xpath(u'//div[@class="flagge"]/a/img/@src').extract()

        flag_url = self.clean_string(flag_info[0]) if flag_info else u''

        # If url is a relative url, builds an absolute url.
        if flag_url and not flag_url.startswith(u'http'):
            flag_url = self.build_tm_url(flag_url)

        # If the url is a default image, sets url to empty string.
        if u'default' in flag_url or u'somebody' in flag_url:
            flag_url = u''

        return [ flag_url ] if flag_url else []


    def get_footballer_injury(self, selector):

        xpath = u'//div[@class="verletzungsbox"]/div[@class="text"]/span/text()'
        end = selector.xpath(xpath).extract()

        if end:
            end_split = end[0].split(u' ')
            if len(end_split) > 3:
                end = [u' '.join(end_split[-3:])]
            else:
                end = [u'unknown']


        xpath = u'//div[@class="verletzungsbox"]/div[@class="text"]/text()'
        info = selector.xpath(xpath).extract()

        injury_info = {
            u'info': self.clean_string(info[0]) if info else u'',
            u'return': self.clean_string(end[0]) if end else u'',
        }

        return injury_info


    def get_footballer_is_captain(self, selector):

        captain = selector.xpath(u'//div[contains(@class, "captain")]').extract()

        return True if captain else False


    def get_footballer_nationalities(self, selector):

        countries = []

        xpath = u'//table[@class="auflistung"]/tr/th[contains(text(),"%s")]/../td/img/@title'
        names = selector.xpath(xpath % 'Nationality').extract()

        xpath = u'//table[@class="auflistung"]/tr/th[contains(text(),"%s")]/../td/img/@src'
        flags = selector.xpath(xpath % 'Nationality').extract()

        # A footballer can have several nationalities.
        for index in range(len(names)):
            one_country = {
                u'image_urls': flags[index].replace(u'verysmall', u'small'),
                u'name': names[index],
            }

            # If url is a relative url, builds an absolute url.
            if not one_country[u'image_urls'].startswith(u'http'):
                one_country[u'image_urls'] = self.build_tm_url(one_country[u'image_urls'])

            # If the url is a default image, sets url to empty string.
            if (u'default' in one_country[u'image_urls'] or
                u'somebody' in one_country[u'image_urls']):
                one_country[u'image_urls'] = u''

            one_country[u'tm_id'] = self.get_tm_id(one_country[u'image_urls'])
            if one_country[u'image_urls']:
                one_country[u'image_urls'] = [ one_country[u'image_urls'] ]
            else:
                one_country[u'image_urls'] = []

            countries.append(one_country)

        return countries


    def get_footballer_is_arrived(self, selector):

        # Gets older team id.
        xpath = u'//div[contains(@class,"special-info")]/a/div[@class="neuzugang"]/../@%s'
        from_team = selector.xpath(xpath % u'href').extract()
        from_id = self.get_tm_id(from_team[0]) if from_team else u''

        # Gets amount info.
        arrived_info = selector.xpath(xpath % u'title').extract()
        amount_info = arrived_info[0].split(u':')[-1] if arrived_info else u''
        amount = u''

        # Processes amount info to get amount.
        if from_id and arrived_info:
            info_splitted = amount_info.split(u' ')
            for item in info_splitted:
                if item in [u'Mill.', u'Th.']:
                    i = info_splitted.index(item)
                    amount = float(info_splitted[i-1].replace(u',', u'.'))
                    amount = amount * 1000 * 1000 if item in [u'Mill.'] else amount * 1000
                    amount = unicode(int(amount))
                    break
                elif item in [u'-', u'Free', u'Libre']:
                    amount = u'0'
                    break
                elif item in [u'?']:
                    amount = None
                    break
                else:
                    pass

        # Gets loan info.
        xpath = u'//div[contains(@class,"special-info")]/a/div[@class="ausgeliehen"]'
        loan_info = selector.xpath(xpath).extract()

        # If the footballer is loaned, sets amount to 'loan'.
        if loan_info:
            amount = u'loan'

        arrived = {
            u'from_team': from_id,
            u'amount': amount,
        }

        return arrived


    def get_footballer_number(self, selector):

        number = selector.xpath(u'//div[@class="rueckennummer-profil"]/text()').extract()

        return self.clean_string(number[0]) if number else u''


    def get_footballer_personal_info(self, selector, attribute):

        if attribute in [u'Date']:
            extra_filter = u'/a'
        elif attribute in [u'Place']:
            extra_filter = u'/span'
        else:
            extra_filter = u''

        xpath = u'//table[@class="auflistung"]/tr/th[contains(text(), "%s")]/../td%s/text()'
        info = selector.xpath(xpath % (attribute, extra_filter)).extract()

        return self.clean_string(info[0]) if info else u''


    def get_footballer_position(self, selector, role):

        xpath = u'//table[@class="auflistung"]/tr/td/normal[contains(text(), "%s")]/../a/text()'
        positions = selector.xpath(xpath % role).extract()

        return positions


    def get_footballer_value(self, selector):

        # Gets value info.
        xpath = u'//div[contains(@class, "marktwert")]/span/a/text()'
        value_info = selector.xpath(xpath).extract()

        # Processes value info to gets a float.
        if value_info and value_info[0] and value_info[0] not in [u'-']:
            value = float(value_info[0].replace(u',', u'.'))
        else:
            value = 0.0

        # Gets base info.
        xpath = u'//div[contains(@class, "marktwert")]/span/a/span/text()'
        base_info = selector.xpath(xpath).extract()
        base = base_info[0] if base_info else u''

        # Gets the real value processing base info.
        if u'Mill.' in base:
            value = value * 1000 * 1000
        elif u'Th.' in base:
            value = value * 1000

        return int(value)


    def get_tm_id(self, base_url):

      slug = u'/saison_id'

      if slug in base_url:
          base_url = base_url.split(slug)[0]

      item_id = base_url.split(u'/')[-1]

      return item_id.split(u'.')[0]


    def get_tm_logo_url(self, selector):

        logo_info = selector.xpath(u'//div[@class="headerfoto"]/img/@src').extract()

        logo_url = self.clean_string(logo_info[0]) if logo_info else u''

        # If url is a relative url, builds an absolute url.
        if logo_url and not logo_url.startswith(u'http'):
            logo_url = self.build_tm_url(logo_url)

        # If the url is a default image, sets url to empty string.
        if u'default' in logo_url or u'somebody' in logo_url:
            logo_url = u''

        return [ logo_url ] if logo_url else []


    def get_tm_name(self, selector):

        name = selector.xpath(u'//div[@class="spielername-profil"]/text()').extract()

        return self.clean_string(name[0]) if name else u''


    def get_tm_url_slug(self, response):

        url = unicode(response.url)

        return url.split(TM_HOST_NAME)[-1] if url else u''


    def get_tm_links(self, response):

        links = []
        selector = scrapy.selector.Selector(response)

        table = selector.xpath(u'//div[@id="yw1"]/table/tbody/tr')
        for one_row in table:

            one_link = one_row.xpath(u'.//td[contains(@class, "hauptlink")]/a/@href').extract()

            if one_link:
                links.extend(one_link)

        return links


    # Function that is executed before spider is closed.
    def spider_closed(self, spider):

        self.log(unicode(self.counters), level=scrapy.log.INFO)
