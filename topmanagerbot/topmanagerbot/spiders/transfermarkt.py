# -*- coding: utf-8 -*-
# topmanagerbot/spiders/transfermarkt.py

#TODO
# pedir confirmacion de los cambios raros
# delete duplicates
# saves items in django database
# not save url image, download it and save it

import os
import scrapy

from topmanagerbot import settings
from topmanagerbot import items


class TransfermarktSpider(scrapy.Spider):

    name = u'transfermarkt'
    allowed_domains = [ settings.TM_HOST_NAME ]
    start_urls = ()
    counters = {
        'countries_processed': 0,
        'leagues_processed': 0,
        'clubs_processed': 0,
        'footballers_processed': 0,
        'injuried_players': 0, #TODO
        'loans': 0, #TODO
        'new_arrivals': 0, #TODO
    }


    def __init__(self):

        for one_league in settings.TM_LEAGUES:

            league_url = self.build_tm_url(one_league)
            self.start_urls = self.start_urls + ( league_url, )

        dispatcher = scrapy.xlib.pydispatch.dispatcher
        dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)
        super(TransfermarktSpider, self).__init__()


    def parse(self, response):

        # Gets country info.
        country = items.Country(self.get_country_info(response))

        yield country

        # Gets league info.
        league = items.League(self.get_league_info(response))
        league['country'] = country['tm_id']

        yield league

        # Gets clubs links and proccess them.
        clubs_links = self.get_tm_links(response)

        meta = {
            'league': league['tm_id'],
        }

        for one_club in clubs_links:

          club_url = self.build_tm_url(one_club)
          yield scrapy.Request(url=club_url, meta=meta, callback=self.parse_club)


    def parse_club(self, response):

        meta = response.meta

        # Gets country info.
        country = items.Country(self.get_country_info(response))

        yield country

        # Gets club info.
        club = items.Club(self.get_club_info(response))
        club['country'] = country['tm_id']
        club['league'] = meta.get('league', settings.DEFAULT_NA)

        yield club

        # Gets footballers links and proccess them.
        footballers_links = self.get_tm_links(response)

        meta = {
            'club': club['tm_id'],
        }

        for one_footballer in footballers_links:

          footballer_url = self.build_tm_url(one_footballer)
          yield scrapy.Request(url=footballer_url, meta=meta, callback=self.parse_footballer)


    def parse_footballer(self, response):

        meta = response.meta

        # Gets nationality info.
        countries = []
        nationalities = self.get_footballer_nationalities(response)
        for one_nationality in nationalities:
            country = items.Country(one_nationality)
            countries.append(one_nationality['tm_id'])

            yield country

        # Gets footballer info.
        footballer = items.Footballer(self.get_footballer_info(response))
        footballer['club'] = meta.get('club', settings.DEFAULT_NA)
        footballer['nationalities'] = ','.join(countries)

        yield footballer


    ###############################################
    ## Functions which build dicts to create items.
    ###############################################
    def get_country_info(self, response):

        selector = scrapy.selector.Selector(response)

        country = {
            u'flag_slug': self.get_country_flag(selector),
            u'name': self.get_country_name(selector),
        }

        # Sets tm_id.
        country[u'tm_id'] = self.get_tm_id(country['flag_slug'])

        return country


    def get_league_info(self, response):

        selector = scrapy.selector.Selector(response)

        league = {
            u'country': u'', # Country is setted in parse function.
            u'logo_slug': self.get_tm_logo_slug(selector),
            u'name': self.get_tm_name(selector),
            u'tm_slug': self.get_tm_url_slug(response),
        }

        # Sets tm_id.
        league[u'tm_id'] = self.get_tm_id(league['tm_slug'])

        return league


    def get_club_info(self, response):

        selector = scrapy.selector.Selector(response)

        club = {
            u'country': u'', # Country is setted in parse_club function.
            u'league': u'', # League is setted in parse_club function.
            u'logo_slug': self.get_tm_logo_slug(selector),
            u'name': self.get_tm_name(selector),
            u'seats_number': self.get_club_seats(selector),
            u'stadium': self.get_club_stadium(selector),
            u'tm_slug': self.get_tm_url_slug(response),
        }

        # Sets tm_id.
        club[u'tm_id'] = self.get_tm_id(club[u'tm_slug'])

        return club


    def get_footballer_info(self, response):

        selector = scrapy.selector.Selector(response)

        footballer = {
            u'arrived_date': self.get_footballer_personal_info(selector, 'since'),
            u'birth_date': self.get_footballer_personal_info(selector, 'Date'),
            u'birth_place': self.get_footballer_personal_info(selector, 'Place'),
            u'photo_slug': self.get_tm_logo_slug(selector),
            u'captain': self.get_footballer_is_captain(selector),
            u'club': u'', # Club is setted in parse_footballer function.
            u'contract_until': self.get_footballer_personal_info(selector, 'until'),
            u'foot': self.get_footballer_personal_info(selector, 'Foot'),
            u'full_name': self.get_footballer_personal_info(selector, 'ame'),
            u'height': self.get_footballer_personal_info(selector, 'Height'),
            u'main_position': self.get_footballer_position(selector, 'Main'),
            u'name': self.get_tm_name(selector),
            u'nationalities': u'', # Nationalities is setted in parse_footballer function.
            u'number': self.get_footballer_number(selector),
            u'secondary_positions': self.get_footballer_position(selector, 'Secondary'),
            u'tm_slug': self.get_tm_url_slug(response),
            u'value': self.get_footballer_value(selector),
        }

        # Sets tm_id.
        footballer[u'tm_id'] = self.get_tm_id(footballer[u'tm_slug'])

        # If does not have full_name, sets name as full_name.
        if footballer[u'full_name'] is settings.DEFAULT_NA:
            footballer[u'full_name'] = footballer['name']

        # Sets arrival info.
        new_arrival = self.get_footballer_is_arrived(selector)
        footballer['new_arrival_from'] = new_arrival['from_team']
        footballer['new_arrival_amount'] = new_arrival['amount']

        # Sets injury info.
        injury = self.get_footballer_injury(selector)
        footballer['injury_info'] = injury['info']
        footballer['injury_return'] = injury['return']

        return footballer


    ################################
    ## Utils to gets the items info.
    ################################

    def build_tm_url(self, slug):

        hosted_url = u'%s/%s' % (settings.TM_HOST_NAME, slug)
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

        seats = selector.xpath('//table[@class="profilheader"]/tr/td/span[contains(text(), "Seats")]/text()').extract()

        if seats:
          seats_number = seats[0].split(' ')[0]
        else:
          seats_number = ''

        return int(seats_number.replace('.','')) if seats_number else 0


    def get_club_stadium(self, selector):

        stadium = selector.xpath('//table[@class="profilheader"]/tr/td/a[contains(@href, "stadion")]/text()').extract()

        return self.clean_string(stadium[0]) if stadium else settings.DEFAULT_NA


    def get_country_name(self, selector):

        name = selector.xpath('//div[@class="flagge"]/a/img/@title').extract()

        return self.clean_string(name[0]) if name else settings.DEFAULT_NA


    def get_country_flag(self, selector):

        flag = selector.xpath('//div[@class="flagge"]/a/img/@src').extract()

        return self.clean_string(flag[0]) if flag else settings.DEFAULT_NA


    def get_footballer_injury(self, selector):

        xpath = '//div[@class="verletzungsbox"]/div[@class="text"]/span/text()'
        end = selector.xpath(xpath).extract()

        xpath = '//div[@class="verletzungsbox"]/div[@class="text"]/text()'
        info = selector.xpath(xpath).extract()

        injury_info = {
            'info': self.clean_string(info[0]) if info else settings.DEFAULT_NA,
            'return': self.clean_string(end[0]) if end else settings.DEFAULT_NA,
        }

        return injury_info


    def get_footballer_is_captain(self, selector):

        captain = selector.xpath('//div[contains(@class, "captain")]').extract()

        return True if captain else False


    def get_footballer_nationalities(self, selector):

        countries = []

        xpath = '//table[@class="auflistung"]/tr/th[contains(text(),"%s")]/../td/img/@title'
        names = selector.xpath(xpath % 'Nationality').extract()

        xpath = '//table[@class="auflistung"]/tr/th[contains(text(),"%s")]/../td/img/@src'
        flags = selector.xpath(xpath % 'Nationality').extract()

        # A footballer can have several nationalities.
        for i in range(len(names)):
            one_country = {
                u'flag_slug': flags[i].replace('verysmall', 'small'),
                u'name': names[i],
            }

            one_country[u'tm_id'] = self.get_tm_id(one_country['flag_slug'])

            countries.append(one_country)

        return countries


    def get_footballer_is_arrived(self, selector):

        # Gets older team id.
        xpath = '//div[contains(@class,"special-info")]/a/div[@class="neuzugang"]/../@%s'
        from_team = selector.xpath(xpath % 'href').extract()
        from_id = self.get_tm_id(from_team[0]) if from_team else u''

        # Gets amount info.
        arrived_info = selector.xpath(xpath % 'title').extract()
        amount_info = arrived_info[0].split(':')[-1] if arrived_info else u''
        amount = None

        # Processes amount info to get amount.
        if from_id and arrived_info:
            info_splitted = amount_info.split(' ')
            for item in info_splitted:
                if item in [u'Mill.', u'Th.']:
                    i = info_splitted.index(item)
                    amount = float(info_splitted[i-1].replace(',','.'))
                    amount = amount * 1000 * 1000 if item in [u'Mill.'] else amount * 1000
                    amount = unicode(int(amount))
                    break
                elif item in [u'-', u'Free', u'Libre']:
                    amount = 0
                    break
                elif item in ['?']:
                    amount = None
                    break
                else:
                    pass

        # Gets loan info.
        xpath = '//div[contains(@class,"special-info")]/a/div[@class="ausgeliehen"]'
        loan_info = selector.xpath(xpath).extract()

        # If the footballer is loaned, sets amount to 'loan'.
        if loan_info:
            amount = 'loan'

        arrived = {
            'from_team': from_id,
            'amount': amount,
        }

        return arrived


    def get_footballer_number(self, selector):

        number = selector.xpath('//div[@class="spielername-profil"]/text()').extract()

        return self.clean_string(number[0]) if number else settings.DEFAULT_NA


    def get_footballer_personal_info(self, selector, attribute):

        if attribute in ['Date']:
            extra_filter = '/a'
        elif attribute in ['Place']:
            extra_filter = '/span'
        else:
            extra_filter = ''

        xpath = '//table[@class="auflistung"]/tr/th[contains(text(), "%s")]/../td%s/text()'
        info = selector.xpath(xpath % (attribute, extra_filter)).extract()

        return self.clean_string(info[0]) if info else settings.DEFAULT_NA


    def get_footballer_position(self, selector, role):

        xpath = '//table[@class="auflistung"]/tr/td/normal[contains(text(), "%s")]/../a/text()'
        positions = selector.xpath(xpath % role).extract()

        return ','.join(positions) if positions else settings.DEFAULT_NA


    def get_footballer_value(self, selector):

        # Gets value info.
        xpath = '//div[contains(@class, "marktwert")]/span/a/text()'
        value_info = selector.xpath(xpath).extract()

        # Processes value info to gets a float.
        if value_info and value_info[0] and value_info[0] not in ['-']:
            value = float(value_info[0].replace(',','.'))
        else:
            value = 0.0

        # Gets base info.
        xpath = '//div[contains(@class, "marktwert")]/span/a/span/text()'
        base_info = selector.xpath(xpath).extract()
        base = base_info[0] if base_info else ''

        # Gets the real value processing base info.
        if 'Mill.' in base:
            value = value * 1000 * 1000
        elif 'Th.' in base:
            value = value * 1000

        return int(value)


    def get_tm_id(self, base_url):

      slug = '/saison_id'

      if slug in base_url:
          base_url = base_url.split(slug)[0]

      item_id = base_url.split('/')[-1]

      return item_id.split('.')[0]


    def get_tm_logo_slug(self, selector):

        logo = selector.xpath('//div[@class="headerfoto"]/img/@src').extract()

        return self.clean_string(logo[0]) if logo else settings.DEFAULT_NA


    def get_tm_name(self, selector):

        name = selector.xpath('//div[@class="spielername-profil"]/text()').extract()

        return self.clean_string(name[0]) if name else settings.DEFAULT_NA


    def get_tm_url_slug(self, response):

        url = unicode(response.url)

        return url.split(settings.TM_HOST_NAME)[-1] if url else settings.DEFAULT_NA


    def get_tm_links(self, response):

        links = []
        selector = scrapy.selector.Selector(response)

        table = selector.xpath(u'//div[@id="yw1"]/table/tbody/tr')
        for one_row in table:

            one_link = one_row.xpath('.//td[contains(@class, "hauptlink")]/a/@href').extract()

            if one_link:
                links.extend(one_link)

        return links


    # Function that is executed before spider is closed.
    def spider_closed(self, spider):

        self.log(unicode(self.counters), level=scrapy.log.INFO)
