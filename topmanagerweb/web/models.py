# -*- coding: utf-8 -*-
# web/models.py

from django.db import models

from api.models import BaseModel


class User(User):
    # Set as custom user in settings.py
    pass


class Badge(BaseModel):
    pass


class Bid(BaseModel):
    #user = ForeignKey(User)
    #footballer = ForeignKey(Market) #NOTE revisar
    pass


class Comment(BaseModel):
    #author = ForeignKey(User)
    #body = TextField
    #notice = ForeignKey(Notice)
    #type = ChoiceField
    #reply_to = ForeignKey(self, blank=True)
    pass


class Community(BaseModel):
    #description = TextField
    #is_open = BooleanField
    #market = ManyToManyField(Footballer, through=u'Market')
    #noticies = ForeignKey(Notice)
    #password = PasswordField
    #users = ManyToManyField(User, through=u'Team')
    pass


class Kit(BaseModel):
    pass


class LineUp(BaseModel):
    #one = ForeignKey(Position)
    #two = ForeignKey(Position)
    #three = ForeignKey(Position)
    #four = ForeignKey(Position)
    #five = ForeignKey(Position)
    #six = ForeignKey(Position)
    #seven = ForeignKey(Position)
    #eight = ForeignKey(Position)
    #nine = ForeignKey(Position)
    #ten = ForeignKey(Position)
    #eleven = ForeignKey(Position)
    pass


class Loan(BaseModel):
    #footballer = ForeignKey(Footballer)
    pass


class Market(BaseModel):
    #initial_value = PositiveSmallIntegerField
    #community = ForeignKey(Community)
    #footballer = ForeignKey(Footballer)
    pass


class Notice(BaseModel):
    #author = ForeignKey(User)
    #body = TextField
    #is_editable = BooleanField
    #is_sticky = BooleanField
    #type = ChoiceField
    pass


class Signing(BaseModel):
    #team = ForeignKey(Team):
    #footballer ForeignKey(Footballer)
    pass


class Sponsor(BaseModel):
    pass


class Squad(BaseModel):
    #is_called = BooleanField
    #is_starting = BooleanField
    pass


class Team(BaseModel):
    #community = ForeignKey(Community)
    #is_admin = BooleanField
    #lineup = ForeignKey(LineUp)
    #players = ManyToManyField(Footballer, through=u'Squad')
    #user = ForeignKey(User)
    pass
