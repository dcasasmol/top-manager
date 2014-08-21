# -*- coding: utf-8 -*-
# api/models.py

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
        ordering = ['name']

    def __str__(self):
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
    flag = models.ImageField(upload_to='flags', default='flags/default-flag.png')
    tm_id = models.CharField(max_length=255, unique=True)


class Position(BaseModel):
    '''This class models a position on the pitch.

    Attributes:
        img (image): Position image, default `default-position.png`.
        pitch_img (image): Pitch base image, default `base-pitch.png`.
        short_name (str): Position short name.

    '''
    img = models.ImageField(upload_to='positions', default='positions/default-position.png')
    pitch_img = models.ImageField(upload_to='positions', default='positions/base-pitch.png')
    short_name = models.CharField(max_length=3)

    class Meta:
        '''Position model metadata.

        Attributes:
            ordering (list of str): Fields to order by in queries.

        '''
        ordering = ['id']


class League(BaseModel):
    '''This class models a league.

    Attributes:
        country (Country): League country.
        logo (image): League logo, default `default-logo.jpg`.
        tm_id (str): League `transfermarkt` id.
        tm_slug (str): League `transfermarkt` slug.

    '''
    country = models.ForeignKey(Country, related_name='leagues', related_query_name='league')
    logo = models.ImageField(upload_to='leagues', default='leagues/default-logo.jpg')
    tm_id = models.CharField(max_length=255, unique=True)
    tm_slug = models.SlugField(max_length=255)

    # @average_age
    # @average_value
    # @foreings_number
    # @less_valious_player
    # @most_valious_player
    # @players_number
    # @clubs_number
    # @total_value


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
    crest = models.ImageField(upload_to='clubs', default='clubs/default-crest.jpg')
    country = models.ForeignKey(Country, related_name='clubs', related_query_name='club')
    league = models.ForeignKey(League, related_name='leagues', related_query_name='league')
    stadium = models.CharField(max_length=255, blank=True, default='')
    seats = models.PositiveIntegerField(blank=True, null=True, default=None)
    tm_id = models.CharField(max_length=255, unique=True)
    tm_slug = models.SlugField(max_length=255)

    # @average_value
    # @average_age
    # @foreings_number
    # @players_number
    # @less_valiuos_player
    # @most_valious_player
    # @total_value


class Injury(BaseModel):
    '''This class models an injury of a footballer.

    Attributes:
        description (str): Injury description.
        duration (int): Injury duration (in weeks).

    '''
    description = models.CharField(max_length=255, blank=True, default='')
    duration = models.PositiveSmallIntegerField(blank=True, null=True, default=None)

    # @end_date
    # @is_expired
    # @extend_injury(weeks)


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
    RIGHT_HANDED = 'right'
    LEFT_HANDED = 'left'
    AMBIDEXTROUS = 'both'
    FOOT_CHOICES = (
        (RIGHT_HANDED, RIGHT_HANDED.capitalize()),
        (LEFT_HANDED, LEFT_HANDED.capitalize()),
        (AMBIDEXTROUS, AMBIDEXTROUS.capitalize()),
    )

    arrived_date = models.DateField(blank=True, null=True, default=None)
    birth_date = models.DateField(blank=True, null=True, default=None)
    birth_place = models.CharField(max_length=255, blank=True, default='')
    photo = models.ImageField(upload_to='footballers', default='footballers/default-photo.jpg')
    captain = models.BooleanField(default=False)
    club = models.ForeignKey(Club, blank=True, null=True, related_name='footballers', related_query_name='footballer')
    contract_until = models.DateField(blank=True, null=True, default=None)
    foot = models.CharField(max_length=255, choices=FOOT_CHOICES, default=None)
    full_name = models.CharField(max_length=255, blank=True, default='') #TODO override save functions to set name here.
    height = models.FloatField(blank=True, null=True, default=None)
    injury = models.OneToOneField(Injury, blank=True, null=True, related_name='footballer')
    # TODO Loan class will be implemented in web app.
    # loan = models.OneToOneField(Loan, blank=True, null=True, related_name='footballer')
    nationalities = models.ManyToManyField(Country, through='Nationality', related_name='footballers', related_query_name='footballer')
    new_arrival_from = models.ForeignKey(Club, blank=True, null=True, related_name='sales', related_query_name='sale')
    new_arrival_price = models.PositiveIntegerField(blank=True, null=True, default=None)
    number = models.CharField(max_length=255, blank=True, default='')
    positions = models.ManyToManyField(Position, through='PlayingPosition', related_name='footballers', related_query_name='footballer')
    tm_id = models.CharField(max_length=255, unique=True)
    tm_slug = models.SlugField(max_length=255)
    value = models.PositiveIntegerField(default=0)

    # @age
    # @is_loaned
    # @is_injuried
    # @is_nationalitied(Country, primary=False)
    # @injury_info
    # @main_position
    # @secondary_positions
    # @extend_contract(years)


class Nationality(BaseModel):
    '''This class is an intermediate model between Footballer and Country.

    Store if the nationality is birth nationality or not.

    Attributes:
        country (Country): Country where is nationalizated.
        footballer (Footballer): Footballer nationalizated.
        primary (bool): If the nationality is primary or not, default False.

    '''
    country = models.ForeignKey(Country, related_name='nationalizated', related_query_name='nationalizated')
    footballer = models.ForeignKey(Footballer, related_name='nationalizated', related_query_name='nationalizated')
    primary = models.BooleanField(default=False)


class PlayingPosition(BaseModel):
    '''This class is an intermediate model between Footballer and Position.

    Store if the position is the main position or not.

    Attributes:
        footballer (Footballer): Footballer who plays in the position.
        position (Position): Position where the footballer plays.
        primary (bool): If the position is primary or not, default False.

    '''
    footballer = models.ForeignKey(Footballer, related_name='playing', related_query_name='playing')
    position = models.ForeignKey(Position, related_name='playing', related_query_name='playing')
    primary = models.BooleanField(default=False)


# Maybe a future functionality of top-manager.
# class Moral(BaseModel):
#     pass
