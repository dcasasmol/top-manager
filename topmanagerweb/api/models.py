# -*- coding: utf-8 -*-
# api/models.py

from django.db import models


class BaseModel(models.Model):
    '''This abstract class models the common attirbutes of a model.

    Attributes:
        id (int): BaseModel id.
        name (str): BaseModel name.
        creation_date (datetime): BaseModel creation datetime.
        last_update (datetime): BaseModel last update datetime.
        active (bool): If the BaseModel is active or not, default True.

    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        '''BaseModel model metadata.

        Attributes:
            abstract (bool): If the class is abstract or not.
            ordering (list of str): Fields to order by in queries.

        '''
        abstract = True
        ordering = ['name']


class Footballer(BaseModel):
    arrived_date = DateField
    birth_date = DateField
    birth_place = CharField
    photo = SlugField #Change to ImageField
    captain = BooleanField
    club = ForeignKeyField(Club, reverse_name='players')
    contract_until
    foot = SelectField('right', 'left', 'both')
    full_name = CharField
    height = FloatField
    injury = ForeignKeyField(Injury, reverse_name='footballer', max=1, blank=True)
    loan = ForeignKeyField(Loan, reverse_name='footballer', max=1, blank=True)
    nationalities = ManyToManyField(Country, through='Nationality')
    new_arrival_from = ForeignKeyField(Club, reverse_name='solds', blank=True)
    new_arrival_amount = IntegerField(blank=True)
    number = CharField
    positions = ManyToManyField(Position, through='') #TODO
    tm_id = CharField
    tm_slug = SlugField
    value = IntegerField

    @age
    @contract_until
    @is_loaned
    @is_injuried
    @is_nationalitied(Country, primary=False)
    @injury_info
    @main_position
    @secondary_positions


class Country(BaseModel):
    tm_id = CharField
    flag_slug = SlugField


class Club(BaseModel):
    stadium = CharField
    logo = SlugField #Change to ImageField
    seats = IntegerField
    country = ForeignKeyField(Country, reverse_name='clubs')
    league = ForeignKeyField(League, reverse_name='clubs')
    tm_id = CharField
    tm_slug = SlugField

    average_value
    average_age
    foreings_number
    players_number
    less_valiuos_player
    most_valious_player
    total_value


class League(BaseModel):
    tm_id = CharField
    tm_slug = SlugField
    logo = SlugField #Change to ImageField
    country = ForeignKeyField(Country, reverse_name='leagues')

    average_age
    average_value
    foreings_number
    less_valiuos_player
    most_valious_player
    players_number
    teams_number
    total_value


class Nationality(BaseModel):
    footballer = ForeignKeyField(Footballer)
    country = ForeignKeyField(Country)
    primary = BooleanField


class Injury(BaseModel):
    description = CharField(blank=True)
    duration = IntegerField(blank=True) #weeks

    @end_date
    @is_expired
    @extend_injury(int) #weeks


class Position(BaseModel):
    pitch_img = ImageField
    img = ImageField

# u'Keeper', GK
# u'Left-Back', LB
# u'Right-Back', RB
# u'Centre Back', CB
# u'Defensive Midfield', DM
# u'Central Midfield', CM
# u'Attacking Midfield', AM
# u'Left Midfield', LM
# u'Right Midfield' RM
# u'Right Wing', RW
# u'Left Wing', LW
# u'Centre Forward', CF
# u'Secondary Striker', SS


# Maybe a future functionality of top-manager.
# class Moral(BaseModel):
#       pass
