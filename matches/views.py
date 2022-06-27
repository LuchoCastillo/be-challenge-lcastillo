from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views import View

from matches.models import Competition, Player, Team
from matches.serializers import PlayerSerializer, TeamSerializer
from matches.third_party import FootballDataAPI

from rest_framework import generics
import requests
import urllib.parse


class ImportLeagueView(View):
    football_api = FootballDataAPI()

    def get(self, request, *args, **kwargs):
        code = kwargs['code']

        # Get or create competition by code
        competition_dict = self.football_api.get_competition(code)
        competition, _ = Competition.objects.get_or_create(
            **competition_dict
        )

        # Create teams
        teams = self.football_api.get_teams(code)
        new_teams_count = 0
        new_players_count = 0

        for team in teams:
            team_id = str(team['id'])
            del team['id']

            new_team, created = Team.objects.get_or_create(
                tla=team['tla'], defaults={'competition': competition, **team}
            )

            if created:
                # Create players for each new team
                players = self.football_api.get_players(team_id)
                players = [
                    Player(dict(player, **{'team': new_team}))
                    for player in players
                ]
                Player.objects.bulk_create(players)

                new_teams_count += 1
                new_players_count += len(players)

        return HttpResponse(f'''
            Imported {competition.name} competition.</br>
            Imported {new_teams_count} teams.</br>
            Imported {new_players_count} players.</br></br>

            There’re {self.football_api.requests_left} requests left for the next {self.football_api.seconds_left} seconds!
        ''')


class PlayerListAPIView(generics.ListAPIView):
    """Returns a list of all players from a certain leagueCode or by team"""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_queryset(self):
        return self.queryset.filter(team__competition__code=self.kwargs['code'])


class TeamRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = 'name'
