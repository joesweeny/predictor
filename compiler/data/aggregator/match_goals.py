import pandas as pd
from datetime import datetime
from compiler.grpc.proto.fixture.fixture_pb2 import Fixture
from compiler.grpc.result_client import ResultClient
from compiler.grpc.proto.result.result_pb2 import Result, MatchStats


class MatchGoals:
    def __init__(self, result_client: ResultClient):
        self.result_client = result_client

    __columns = [
        'matchID',
        'round',
        'date',
        'season',
        'homeTeam',
        'homeGoals',
        'awayTeam',
        'awayGoals',
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

        date = pd.to_datetime(datetime.utcfromtimestamp(result.date_time), format='%Y-%m-%dT%H:%M:%S')

        data = {
            'matchID': result.id,
            'round': result.round.name,
            'date': date,
            'season': result.season.name,
            'homeTeam': home_team.name,
            'homeGoals': self.__get_value('home_score', match_stats),
            'awayTeam': away_team.name,
            'awayGoals': self.__get_value('away_score', match_stats),
        }

        return data

    @staticmethod
    def __get_value(prop: str, stats: MatchStats):
        if stats.HasField(prop):
            p = getattr(stats, prop)
            return p.value

        return
