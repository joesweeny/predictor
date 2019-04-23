import pandas as pd
from predictor.grpc.result_client import ResultClient


class MatchGoals:
    def __init__(self, client: ResultClient):
        self.result_client = client

    __columns = [
        'Match ID',
        'Home Team ID',
        'Away Team ID',
        'Competition ID',
        'Is Cup',
        'Season ID',
        'Is Current Season',
        'Referee ID',
        'Venue ID',
        'Date',
        'Home Days Since Last Match',
        'Away Days Since Last Match',
        'Home League Position',
        'Away League Position',
        'Home Formation',
        'Away Formation',
        'Home Avg Goals Scored Last 20',
        'Home Avg Goals Conceded Last 20',
        'Away Avg Goals Scored Last 20',
        'Away Avg Goals Conceded Last 20',
        'Home Goals in Lineup',
        'Away Goals in Lineup',
        'Average Goals for Fixture',
        'Total Goals in Match',
    ]

    def ForSeason(self, season_id):
        df = pd.DataFrame(columns=self.__columns)

        df = df.append(self.__resultToRow(), ignore_index=True)

        for result in self.result_client.GetResultsForSeason(season_id):
            print(result)

        return df

    def __resultToRow(self):
        # competition = result.competition
        # season = result.season
        # match_data = result.match_data
        # match_stats = match_data.stats

        # data = [
        #     result.id,
        #     competition.id,
        #     competition.is_cup.value,
        #     season.id,
        #     season.is_current.value,
        #     result.referee_id.value,
        #     result.venue.id.value,
        #     result.date_time,
        #     'Calculate Home Days',
        #     'Calculate Away Days',
        #     match_data.home_team.id,
        #     match_data.away_team.id,
        #     match_stats.home_league_position.value,
        #     match_stats.away_league_position.value,
        #     match_stats.home_formation.value,
        #     match_stats.away_formation.value,
        #     'Calculate Home Goals Scored',
        #     'Calculate Away Goals Scored',
        #     'Calculate Home Goals Conceded',
        #     'Calculate Away Goals Conceded',
        #     'Calculate Home Goals in Lineup',
        #     'Calculate Away Goals in Lineup',
        #     'Calculate Average Goals for Fixture',
        #     self.__calculateGoalsInMatch(match_stats.home_score.value, match_stats.away_score.value)
        # ]

        data = {
            'Match ID': 66,
            'Home Team ID': 7901,
            'Away Team ID': 496,
            'Competition ID': 55,
            'Is Cup': False,
            'Season ID': 39910,
            'Is Current Season': True,
            'Referee ID': 3412,
            'Venue ID': 88,
            'Date': 1556043338,
            'Home Days Since Last Match': 'Calculate Home Days',
            'Away Days Since Last Match': 'Calculate Away Days',
            'Home League Position': 3,
            'Away League Position': 15,
            'Home Formation': '4-4-2',
            'Away Formation': '5-3-1-1',
            'Home Avg Goals Scored Last 20': 'Calculate Home Goals Scored',
            'Home Avg Goals Conceded Last 20': 'Calculate Away Goals Scored',
            'Away Avg Goals Scored Last 20': 'Calculate Home Goals Conceded',
            'Away Avg Goals Conceded Last 20': 'Calculate Away Goals Conceded',
            'Home Goals in Lineup': 'Calculate Home Goals in Lineup',
            'Away Goals in Lineup': 'Calculate Away Goals in Lineup',
            'Average Goals for Fixture': 'Calculate Average Goals for Fixture',
            'Total Goals in Match': 4,
        }

        return data

    @staticmethod
    def __calculateGoalsInMatch(home_goals, away_goals):
        if home_goals is None or away_goals is None:
            return

        return home_goals + away_goals
