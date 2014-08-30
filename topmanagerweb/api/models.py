# -*- coding: utf-8 -*-
# api/models.py

import datetime

from django.db import models


class BaseModel(models.Model):
    '''This abstract class models the common attributes of a model.

    Attributes:
        id (int): BaseModel id.
        name (str): BaseModel name.
        creation_date (datetime): BaseModel creation datetime.
        last_update (datetime): BaseModel last update datetime.
        is_active (bool): If the BaseModel is active or not, default True.

    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        '''BaseModel model metadata.

        Attributes:
            abstract (bool): If the class is abstract or not.
            ordering (list of str): Fields to order by in queries.

        '''
        abstract = True
        ordering = [u'name']

    def __unicode__(self):
        '''Displays a human-readable representation of the BaseModel object.

        Returns:
            str: Human-readable representation of the BaseModel object.

        '''
        return self.name


class Country(BaseModel):
    '''This class models a country.

    Attributes:
        flag (image): Country flag, default `default-flag.png`.
        tm_id (str): Country `transfermarkt` id.

    '''
    flag = models.ImageField(upload_to=u'flags', default=u'flags/default-flag.png')
    tm_id = models.CharField(max_length=255, unique=True)

    class Meta:
        '''Country model metadata.

        Attributes:
            ordering (list of str): Fields to order by in queries.
            verbose_name_plural (str): Plural name for the object.

        '''
        ordering = [u'name']
        verbose_name_plural = u'countries'


class Position(BaseModel):
    '''This class models a position on the pitch.

    Attributes:
        img (image): Position image, default `default-position.png`.
        pitch_img (image): Pitch base image, default `base-pitch.png`.
        short_name (str): Position short name.

    '''
    img = models.ImageField(upload_to=u'positions', default=u'positions/default-position.png')
    pitch_img = models.ImageField(upload_to=u'positions', default=u'positions/base-pitch.png')
    short_name = models.CharField(max_length=3)

    class Meta:
        '''Position model metadata.

        Attributes:
            ordering (list of str): Fields to order by in queries.

        '''
        ordering = [u'id']


class League(BaseModel):
    '''This class models a league.

    Attributes:
        country (Country): League country.
        logo (image): League logo, default `default-logo.jpg`.
        tm_id (str): League `transfermarkt` id.
        tm_slug (str): League `transfermarkt` slug.

    '''
    country = models.ForeignKey(Country, related_name=u'leagues', related_query_name=u'league')
    logo = models.ImageField(upload_to=u'leagues', default=u'leagues/default-logo.jpg')
    tm_id = models.CharField(max_length=255, unique=True)
    tm_slug = models.SlugField(max_length=255)

    @property
    def average_age(self):
        '''Gets the average age of the league.

        Returns:
            int: Average age.

        '''
        sum_age = 0

        for one_club in self.clubs.all():
            sum_age += one_club.average_age

        return int(round(sum_age / self.clubs_number))

    @property
    def average_value(self):
        '''Gets the average value of the league.

        Returns:
            int: Average value.

        '''
        sum_value = 0

        for one_club in self.clubs.all():
            sum_value += one_club.total_value

        return int(round(sum_value / self.footballers_number))

    @property
    def clubs_number(self):
        '''Gets the clubs number on the league.

        Returns:
            int: Clubs number.

        '''
        return self.clubs.count()

    @property
    def footballers_number(self):
        '''Gets the footballers number on the league.

        Returns:
            int: Footballers number.

        '''
        sum_value = 0

        for one_club in self.clubs.all():
            sum_value += one_club.footballers_number

        return sum_value

    @property
    def foreigns_number(self):
        '''Gets the foreigns number on the league.

        Returns:
            int: Foreigns number.

        '''
        foreigns_number = 0

        for one_club in self.clubs.all():
            foreigns_number += one_club.foreigns_number

        return foreigns_number

    @property
    def less_valious_footballer(self):
        '''Gets the less valious footballer of the league.

        Returns:
            Footballer: Less valious footballer.

        '''
        less = self.clubs.first().less_valious_footballer

        for one_club in self.clubs.all():
            if one_club.less_valious_footballer.value < less.value:
                less = one_club.less_valious_footballer

        return less

    @property
    def most_valious_footballer(self):
        '''Gets the most valious footballer of the league.

        Returns:
            Footballer: Most valious footballer.

        '''
        most = self.clubs.first().most_valious_footballer

        for one_club in self.clubs.all():
            if one_club.most_valious_footballer.value > most.value:
                most = one_club.most_valious_footballer

        return most

    @property
    def total_value(self):
        '''Gets the total value of the league.

        Returns:
            int: Total value.

        '''
        sum_value = 0

        for one_club in self.clubs.all():
            sum_value += one_club.total_value

        return sum_value


class Club(BaseModel):
    '''This class models a club.

    Attributes:
        crest (image): Club crest, default `default-crest.jpg`.
        country (Country): Club country.
        league (League): Club league.
        stadium (str, optional): Stadium name, default empty string.
        seats (int, optional): Stadium seats number, default 0.
        tm_id (str): Club `transfermarkt` id.
        tm_slug (str): Club `transfermarkt` slug.

    '''
    crest = models.ImageField(upload_to=u'clubs', default=u'clubs/default-crest.jpg')
    country = models.ForeignKey(Country, related_name=u'clubs', related_query_name=u'club')
    league = models.ForeignKey(League, related_name=u'clubs', related_query_name=u'club')
    stadium = models.CharField(max_length=255, blank=True, default=u'')
    seats = models.PositiveIntegerField(blank=True, null=True, default=None)
    tm_id = models.CharField(max_length=255, unique=True)
    tm_slug = models.SlugField(max_length=255)

    @property
    def average_value(self):
        '''Gets the average value of the club.

        Returns:
            int: Average value.

        '''
        return int(round(self.footballers.aggregate(avg=models.Avg('value'))['avg']))

    @property
    def average_age(self):
        '''Gets the average age of the club.

        Returns:
            int: Average age.

        '''
        sum_age = 0

        for one_footballer in self.footballers.all():
            sum_age += one_footballer.age

        return int(round(sum_age / self.footballers.count()))

    @property
    def foreigns_number(self):
        '''Gets the foreigns number on the club.

        Returns:
            int: Foreigns number.

        '''
        foreigns_number = 0

        for one_footballer in self.footballers.all():
            if not one_footballer.is_nationalitied(self.league.country, True):
                foreigns_number += 1

        return foreigns_number

    @property
    def footballers_number(self):
        '''Gets the footballers number on the club.

        Returns:
            int: Footballers number.

        '''
        return self.footballers.count()

    @property
    def less_valious_footballer(self):
        '''Gets the less valious footballer of the club.

        Returns:
            Footballer: Less valious footballer.

        '''
        min_value = self.footballers.aggregate(min=models.Min('value'))['min']

        return self.footballers.filter(value=min_value).first()

    @property
    def most_valious_footballer(self):
        '''Gets the most valious footballer of the club.

        Returns:
            Footballer: Most valious footballer.

        '''
        max_value = self.footballers.aggregate(max=models.Max('value'))['max']

        return self.footballers.filter(value=max_value).first()

    @property
    def total_value(self):
        '''Gets the total value of the club.

        Returns:
            int: Total value.

        '''
        return self.footballers.aggregate(sum=models.Sum('value'))['sum']


class Injury(BaseModel):
    '''This class models an injury of a footballer.

    Attributes:
        description (str): Injury description.
        duration (int, optional): Injury duration (in weeks).

    '''
    description = models.CharField(max_length=255, blank=True, default=u'')
    duration = models.PositiveSmallIntegerField(blank=True, null=True, default=None)

    class Meta:
        '''Injury model metadata.

        Attributes:
            verbose_name_plural (str): Plural name for the object.

        '''
        verbose_name_plural = u'injuries'

    def extend_injury(self, weeks):
        '''Extend the injury duration.

        Args:
            weeks (int): Weeks number to extend.

        Returns:
            date: New return date.

        '''
        if weeks > 0:
            self.duration += weeks
            self.save()

        return self.return_date

    @property
    def info(self):
        '''Gets the injury info.

        Returns:
            str: Injury info.

        '''
        return self.description if self.description else u'Unknown'

    @property
    def is_expired(self):
        '''Check if the injury is expired.

        Returns:
            bool: True if expired, False otherwise.

        '''
        return datetime.date.today() > self.return_date if self.return_date else False

    @property
    def return_date(self):
        '''Gets the injury return date.

        Returns:
            date: Injury return date.

        '''
        if self.duration is None:
            return_date = self.duration
        else:
            today = datetime.date.today()
            return_date = today + datetime.timedelta(weeks = self.duration)

            # Gets the next weekend of the return date.
            while return_date.weekday() != 5:
                return_date += datetime.timedelta(days=1)

        return return_date


class Footballer(BaseModel):
    '''This class models a footballer.

    Attributes:
        RIGHT_HANDED (str): Right-handed footballer database token.
        LEFT_HANDED (str): Left-handed footballer database token.
        AMBIDEXTROUS: (str): Ambidextrous footballer database token.
        FOOT_CHOICES (tuple): Database foot choices.
        arrived_date (date, optional): Footballer arrived date to the club, default None.
        birth_date (date, optional): Footballer birth date, default None.
        birth_place (str, optional): Footballer birth place, default empty string.
        photo (image): Footballer photo, default `default-photo.jpg`.
        captain (bool): If the footballer is captain or not, default False.
        club (Club, optional): Footballer club.
        contract_until (date, optional): Footballer contract end date, default None.
        foot (str): Footballer foot, select one of `FOOT_CHOICES`, default None.
        full_name (str, optional): Footballer full name, default `name`.
        height (float, optional): Footballer height.
        injury (Injury, optional): Footballer injury.
        loan (Loan, optional): Footballer loan.
        nationalities (list of Country): Footballer nationalities.
        new_arrival_from (Club, optional): Footballer old club.
        new_arrival_price (int, optional): Footballer signing price, default None.
        number (str, optional): Footballer number.
        positions (list of Position): Footballer positions.
        tm_id (str): Footballer `transfermarkt` id.
        tm_slug (str): Footballer `transfermarkt` slug.
        value (int): Footballer value.

    '''
    RIGHT_HANDED = u'right'
    LEFT_HANDED = u'left'
    AMBIDEXTROUS = u'both'
    FOOT_CHOICES = (
        (RIGHT_HANDED, RIGHT_HANDED.capitalize()),
        (LEFT_HANDED, LEFT_HANDED.capitalize()),
        (AMBIDEXTROUS, AMBIDEXTROUS.capitalize()),
    )

    arrived_date = models.DateField(blank=True, null=True, default=None)
    birth_date = models.DateField(blank=True, null=True, default=None)
    birth_place = models.CharField(max_length=255, blank=True, default=u'')
    photo = models.ImageField(upload_to=u'footballers', default=u'footballers/default-photo.jpg')
    captain = models.BooleanField(default=False)
    club = models.ForeignKey(Club, blank=True, null=True, related_name=u'footballers', related_query_name=u'footballer')
    contract_until = models.DateField(blank=True, null=True, default=None)
    foot = models.CharField(max_length=255, choices=FOOT_CHOICES, default=None)
    full_name = models.CharField(max_length=255, blank=True, default=u'')
    height = models.FloatField(blank=True, null=True, default=None)
    injury = models.OneToOneField(Injury, blank=True, null=True, related_name=u'footballer')
    nationalities = models.ManyToManyField(Country, through=u'Nationality', related_name=u'footballers', related_query_name=u'footballer')
    new_arrival_from = models.ForeignKey(Club, blank=True, null=True, related_name=u'sales', related_query_name=u'sale')
    new_arrival_price = models.PositiveIntegerField(blank=True, null=True, default=None)
    number = models.CharField(max_length=255, blank=True, default=u'')
    positions = models.ManyToManyField(Position, through=u'PlayingPosition', related_name=u'footballers', related_query_name=u'footballer')
    tm_id = models.CharField(max_length=255, unique=True)
    tm_slug = models.SlugField(max_length=255)
    value = models.PositiveIntegerField(default=0)

    @property
    def age(self):
        '''Gets the age of the footballer.

        Returns:
            int: Footballer's age.

        '''
        today = datetime.date.today()

        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    @property
    def is_injuried(self):
        '''Checks if the user is injuried.

        Returns:
            bool: True if injuried, False otherwise.

        '''
        return True if self.injury else False

    def is_nationalitied(self, country, primary=False):
        '''Check if the user is nationalitied on the country.

        Args:
            country (Country): Country to check.
            primary (bool, optional): If the nationalization must be primary.

        Returns:
            bool: True if nationalitied, False otherwise.

        '''
        return country in self.nationalities.all()

    @property
    def main_nationality(self):
        '''Gets the main nationality of the footballer.

        Returns:
            Position: Main nationality.

        '''
        return self.nationalizated.filter(primary=True).first().country

    @property
    def main_position(self):
        '''Gets the main position of the footballer.

        Returns:
            Position: Main position.

        '''
        return self.playing.filter(primary=True).first().position

    def extend_contract(self, years):
        '''Extend the contract of the footballer.

        Args:
            years (int): Years number to extend.

        Returns:
            date: New contract end date.

        '''
        if years > 0:
            new_end_year = self.contract_until.year + years
            self.contract_until = self.contract_until.replace(year = new_end_year)
            self.save()

        return self.contract_until

    def save(self, *args, **kwargs):
        '''Saves the Footballer object setting the full_name attribute.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        '''
        if not self.id and not self.full_name:
            self.full_name = self.name

        super(Footballer, self).save(*args, **kwargs)


class Nationality(BaseModel):
    '''This class is an intermediate model between Footballer and Country.

    Store if the nationality is birth nationality or not.

    Attributes:
        country (Country): Country where is nationalizated.
        footballer (Footballer): Footballer nationalizated.
        primary (bool): If the nationality is primary or not, default False.

    '''
    country = models.ForeignKey(Country, related_name=u'nationalizated', related_query_name=u'nationalizated')
    footballer = models.ForeignKey(Footballer, related_name=u'nationalizated', related_query_name=u'nationalizated')
    primary = models.BooleanField(default=False)

    class Meta:
        '''Nationality model metadata.

        Attributes:
            ordering (list of str): Fields to order by in queries.
            verbose_name_plural (str): Plural name for the object.

        '''
        ordering = [u'name']
        verbose_name_plural = u'nationalities'

    def save(self, *args, **kwargs):
        '''Saves the Nationality object setting the name attribute.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        '''
        self.name = u'%s - %s' % (self.footballer.name, self.country.name)

        super(Nationality, self).save(*args, **kwargs)


class PlayingPosition(BaseModel):
    '''This class is an intermediate model between Footballer and Position.

    Store if the position is the main position or not.

    Attributes:
        footballer (Footballer): Footballer who plays in the position.
        position (Position): Position where the footballer plays.
        primary (bool): If the position is primary or not, default False.

    '''
    footballer = models.ForeignKey(Footballer, related_name=u'playing', related_query_name=u'playing')
    position = models.ForeignKey(Position, related_name=u'playing', related_query_name=u'playing')
    primary = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        '''Saves the PlayingPosition object setting the name attribute.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        '''
        self.name = u'%s - %s' % (self.footballer.name, self.position.name)

        super(PlayingPosition, self).save(*args, **kwargs)


# Maybe a future functionality of top-manager.
# class Moral(BaseModel):
#     pass
