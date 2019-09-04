import pandas as pd
from datetime import datetime
from compiler.grpc.proto.fixture.fixture_pb2 import Fixture
from compiler.grpc.result_client import ResultClient
from compiler.grpc.team_stats_client import TeamStatsClient
from compiler.grpc.proto.result.result_pb2 import Result, MatchStats


class MatchGoals:
    def __init__(self, result_client: ResultClient, team_stats_client: TeamStatsClient):
        self.result_client = result_client
        self.team_stats_client = team_stats_client

    __columns = [
        'matchID',
        'round',
        'date',
        'season',
        'homeTeam',
        'homeGoals',
        'homeShotsTotal',
        'homeShotsOnGoal',
        'homeSaves',
        'awayTeam',
        'awayGoals',
        'awayShotsTotal',
        'awayShotsOnGoal',
        'awaySaves'
    ]

    def for_season(self, season_id: int, date_before: datetime) -> pd.DataFrame:
        df = pd.DataFrame(columns=self.__columns)

        results = self.result_client.get_results_for_season(
            season_id=season_id,
            date_before=date_before.isoformat()
        )

        for result in results:
            df = df.append(self.__result_to_row(result), ignore_index=True)

        return df

    def for_fixture(self, fixture: Fixture) -> pd.DataFrame:
        df = pd.DataFrame(columns=self.__columns)

        df = df.append(self.__fixture_to_row(fixture), ignore_index=True)

        return df

    @staticmethod
    def __fixture_to_row(fixture: Fixture) -> dict:
        home_team = fixture.home_team
        away_team = fixture.away_team

        date = pd.to_datetime(datetime.utcfromtimestamp(fixture.date_time), format='%Y-%m-%dT%H:%M:%S')

        data = {
            'matchID': fixture.id,
            'round': fixture.round.name,
            'date': date,
            'season': fixture.season.name,
            'homeTeam': home_team.name,
            'awayTeam': away_team.name,
        }

        return data

    def __result_to_row(self, result: Result) -> dict:
        match_data = result.match_data
        match_stats = match_data.stats
        home_team = match_data.home_team
        away_team = match_data.away_team

        stats = self.team_stats_client.get_team_stats_for_fixture(fixture_id=result.id)

        home_stats = stats.home_team
        away_stats = stats.away_team

        date = pd.to_datetime(datetime.utcfromtimestamp(result.date_time), format='%Y-%m-%dT%H:%M:%S')

        data = {
            'matchID': result.id,
            'round': result.round.name,
            'date': date,
            'season': result.season.name,
            'homeTeam': home_team.name,
            'homeGoals': self.__get_value('home_score', match_stats),
            'homeShotsTotal': self.__get_value('shots_total', home_stats),
            'homeShotsOnGoal': self.__get_value('shots_on_goal', home_stats),
            'homeSaves': self.__get_value('saves', home_stats),
            'awayTeam': away_team.name,
            'awayGoals': self.__get_value('away_score', match_stats),
            'awayShotsTotal': self.__get_value('shots_total', away_stats),
            'awayShotsOnGoal': self.__get_value('shots_on_goal', away_stats),
            'awaySaves': self.__get_value('saves', away_stats),
        }

        return data

    @staticmethod
    def __get_value(prop: str, stats: MatchStats):
        if stats.HasField(prop):
            p = getattr(stats, prop)
            return p.value

        return
