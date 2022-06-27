import requests


class FootballDataAPI:
    """Third party API integration for `football-data.org`.

    Example:
        Instantiate API and request a league.

        >>> api = FootballDataAPI()
        >>> api.get_competition('CL')
        {'name': 'UEFA Champions League', 'code': 'CL', 'area_name': 'Europe'}
    """
    BASE_URL = 'https://api.football-data.org/v2/'
    API_TOKEN = '3e71bdec324c48ae974c978a7a001085'
    requests_left = None
    seconds_left = None

    def _get_call(self, *params):
        response = requests.get(
            '/'.join((self.BASE_URL, *params)), headers={'X-Auth-Token': self.API_TOKEN}
        )

        if response.ok:
            self.seconds_left = response.headers['X-RequestCounter-Reset']
            self.requests_left = response.headers['X-Requests-Available-Minute']

        return response

    def get_competition(self, code):
        response = self._get_call('competitions', code)

        if response.ok:
            json = response.json()
            competition = {
                'name': json['name'],
                'code': code,
                'area_name': json['area']['name'],
            }
        else:
            competition = {}

        return competition

    def get_teams(self, code):
        """Returns the list of teams in a league."""
        response = self._get_call('competitions', code, 'teams')

        if response.ok:
            teams = [
                {
                    'id': team['id'],
                    'name': team['name'],
                    'tla': team['tla'],
                    'short_name': team['shortName'],
                    'area_name': team['area']['name'],
                    'email': team['email'],
                }
                for team in response.json().get('teams', [])
            ]
        else:
            teams = []

        return teams

    def get_players(self, team_id):
        """Returns the list of players in a team."""
        response = self._get_call('teams', team_id)

        if response.ok:
            players = [
                {
                    'name': player['name'],
                    'position': player['position'],
                    'date_of_birth': player['dateOfBirth'],
                    'country_of_birth': player['countryOfBirth'],
                    'nationality': player['nationality'],
                }
                for player in response.json().get('squad', [])
            ]
        else:
            players = []

        return players
