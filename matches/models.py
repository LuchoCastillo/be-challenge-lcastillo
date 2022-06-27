from django.db import models


class Competition(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=8, unique=True)
    area_name = models.CharField(max_length=256, null=True)


class Team(models.Model):
    name = models.CharField(max_length=256)
    tla = models.CharField(max_length=8, unique=True, null=True)
    short_name = models.CharField(max_length=256, null=True)
    area_name = models.CharField(max_length=256, null=True)
    email = models.CharField(max_length=256, null=True)
    competition = models.ForeignKey('matches.Competition', on_delete=models.SET_DEFAULT, default=None)


class Player(models.Model):
    name = models.CharField(max_length=256)
    position = models.CharField(max_length=256)
    date_of_birth = models.DateField(null=True)
    country_of_birth = models.CharField(max_length=256, null=True)
    nationality = models.CharField(max_length=256, null=True)
    team = models.ForeignKey('matches.Team', on_delete=models.SET_DEFAULT, default=None)
