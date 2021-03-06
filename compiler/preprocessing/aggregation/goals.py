import pandas as pd
from datetime import datetime
from compiler.grpc.proto.fixture_pb2 import Fixture
from compiler.grpc.fixture_client import FixtureClient
from compiler.grpc.result_client import ResultClient
from compiler.grpc.team_stats_client import TeamStatsClient
from compiler.grpc.proto.result_pb2 import Result, MatchStats


class GoalsAggregator:
    def __init__(
        self,
        fixture_client: FixtureClient,
        result_client: ResultClient,
        team_stats_client: TeamStatsClient
    ):
        self.fixture_client = fixture_client
        self.result_client = result_client
        self.team_stats_client = team_stats_client

    __columns = [
        'fixtureID',
        'round',
        'date',
        'season',
        'homeTeam',
        'homeGoals',
        'homeXG',
        'homeShotsTotal',
        'homeShotsOnGoal',
        'awayTeam',
        'awayGoals',
        'awayXG',
        'awayShotsTotal',
        'awayShotsOnGoal',
    ]

    def for_season(self, season_id: int, date_before: datetime) -> pd.DataFrame:
        df = pd.DataFrame(columns=self.__columns)

        results = self.result_client.get_results_for_season(
            season_id=season_id,
            date_before=date_before.isoformat()
        )

        for result in results:
            try:
                df = df.append(self.__result_to_row(result), ignore_index=True)
            except Exception:
                continue

        return df

    def for_fixture(self, fixture_id: int) -> (Fixture, pd.DataFrame):
        try:
            fixture = self.fixture_client.get_fixture_by_id(fixture_id=fixture_id)
        except Exception:
            raise Exception("Unable to fetch data for Fixture with ID " + str(fixture_id))

        df = pd.DataFrame(columns=self.__columns)

        df = df.append(self.__fixture_to_row(fixture), ignore_index=True)

        return fixture, df

    @staticmethod
    def __fixture_to_row(fixture: Fixture) -> dict:
        home_team = fixture.home_team
        away_team = fixture.away_team

        date = pd.to_datetime(datetime.utcfromtimestamp(fixture.date_time.utc), format='%Y-%m-%dT%H:%M:%S')

        data = {
            'fixtureID': fixture.id,
            'round': fixture.round.name,
            'date': date,
            'season': fixture.season.name,
            'homeTeam': home_team.name,
            'awayTeam': away_team.name,
        }

        return data

    def __result_to_row(self, result: Result) -> dict:
        match_stats = result.stats
        home_team = result.home_team
        away_team = result.away_team

        stats = self.team_stats_client.get_team_stats_for_fixture(fixture_id=result.id)

        home_stats = stats.home_team
        away_stats = stats.away_team
        xg = stats.team_xg

        date = pd.to_datetime(datetime.utcfromtimestamp(result.date_time.utc), format='%Y-%m-%dT%H:%M:%S')

        data = {
            'fixtureID': result.id,
            'round': result.round.name,
            'date': date,
            'season': result.season.name,
            'homeTeam': home_team.name,
            'homeGoals': self.__get_value('home_score', match_stats),
            'homeXG': self.__get_value('home', xg),
            'homeShotsTotal': self.__get_value('shots_total', home_stats),
            'homeShotsOnGoal': self.__get_value('shots_on_goal', home_stats),
            'awayTeam': away_team.name,
            'awayGoals': self.__get_value('away_score', match_stats),
            'awayXG': self.__get_value('away', xg),
            'awayShotsTotal': self.__get_value('shots_total', away_stats),
            'awayShotsOnGoal': self.__get_value('shots_on_goal', away_stats),
        }

        return data

    @staticmethod
    def __get_value(prop: str, stats: MatchStats):
        if stats.HasField(prop):
            p = getattr(stats, prop)
            return p.value

        return
