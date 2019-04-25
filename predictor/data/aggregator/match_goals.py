import pandas as pd
from predictor.grpc.result_client import ResultClient
from predictor.grpc.proto.result.result_pb2 import Result
from predictor.data import calculator


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

    def ForSeason(self, season_id: int) -> pd.DataFrame:
        df = pd.DataFrame(columns=self.__columns)

        for result in self.result_client.GetResultsForSeason(season_id):
            df = df.append(self.__resultToRow(result), ignore_index=True)

        return df

    @staticmethod
    def __resultToRow(result: Result) -> dict:
        competition = result.competition
        season = result.season
        match_data = result.match_data
        match_stats = match_data.stats

        data = {
            'Match ID': result.id,
            'Home Team ID': match_data.home_team.id,
            'Away Team ID': match_data.away_team.id,
            'Competition ID': competition.id,
            'Is Cup': competition.is_cup.value,
            'Season ID': season.id,
            'Is Current Season': season.is_current.value,
            'Referee ID': result.referee_id.value,
            'Venue ID': result.venue.id.value,
            'Date': result.date_time,
            'Home Days Since Last Match': 'Calculate Home Days',
            'Away Days Since Last Match': 'Calculate Away Days',
            'Home League Position': match_stats.home_league_position.value,
            'Away League Position': match_stats.away_league_position.value,
            'Home Formation': match_stats.home_formation.value,
            'Away Formation': match_stats.away_formation.value,
            'Home Avg Goals Scored Last 20': 'Calculate Home Goals Scored',
            'Home Avg Goals Conceded Last 20': 'Calculate Away Goals Scored',
            'Away Avg Goals Scored Last 20': 'Calculate Home Goals Conceded',
            'Away Avg Goals Conceded Last 20': 'Calculate Away Goals Conceded',
            'Home Goals in Lineup': 'Calculate Home Goals in Lineup',
            'Away Goals in Lineup': 'Calculate Away Goals in Lineup',
            'Average Goals for Fixture': 'Calculate Average Goals for Fixture',
            'Total Goals in Match': calculator.TotalGoalsForMatch(match_stats),
        }

        return data
