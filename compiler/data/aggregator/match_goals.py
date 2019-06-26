import pandas as pd
from datetime import datetime
from compiler.grpc.proto.fixture.fixture_pb2 import Fixture
from compiler.grpc.result_client import ResultClient
from compiler.grpc.proto.result.result_pb2 import Result
from compiler.grpc.team_stats_client import TeamStatsClient
from compiler.grpc.proto.stats.team.stats_pb2 import TeamStats
from compiler.data import calculator


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
        'homeAvgScored',
        'homeAvgConceded',
        'awayTeam',
        'awayGoals',
        'awayAvgScored',
        'awayAvgConceded',
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

    def __fixture_to_row(self, fixture: Fixture):
        home_team = fixture.home_team
        away_team = fixture.away_team

        date = pd.to_datetime(datetime.utcfromtimestamp(fixture.date_time), format='%Y-%m-%dT%H:%M:%S')

        home_previous_results = self.__get_previous_results(date, home_team.id, 5)
        away_previous_results = self.__get_previous_results(date, away_team.id, 5)

        historical_results = self.__get_historical_results(
            date_before=date,
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            limit=10
        )

        data = {
            'matchID': fixture.id,
            'round': fixture.round.name,
            'date': date,
            'season': fixture.season.name,
            'averageGoalsForFixture': calculator.AverageGoalsForResults(
                historical_results
            ),
            'homeTeamID': home_team.id,
            'homeTeam': home_team.name,
            'homeDaysSinceLastMatch': calculator.days_between_results(
                date,
                home_previous_results[0],
            ),
            'homeAvgScoredLast5': calculator.AverageGoalsScoredByTeam(
                home_previous_results,
                home_team.id
            ),
            'homeAvgConcededLast5': calculator.AverageGoalsConcededByTeam(
                home_previous_results,
                home_team.id
            ),
            'homeScoredLastMatch': calculator.GoalsScoredInMatch(
                home_previous_results[0],
                home_team.id
            ),
            'homeConcededLastMatch': calculator.GoalsConcededInMatch(
                home_previous_results[0],
                home_team.id
            ),
            'awayTeamID': away_team.id,
            'awayTeam': away_team.name,
            'awayDaysSinceLastMatch': calculator.days_between_results(
                date,
                away_previous_results[0]
            ),
            'awayAvgScoredLast5': calculator.AverageGoalsScoredByTeam(
                away_previous_results,
                away_team.id
            ),
            'awayAvgConcededLast5': calculator.AverageGoalsConcededByTeam(
                away_previous_results,
                away_team.id
            ),
            'awayScoredLastMatch': calculator.GoalsScoredInMatch(
                away_previous_results[0],
                away_team.id
            ),
            'awayConcededLastMatch': calculator.GoalsConcededInMatch(
                away_previous_results[0],
                away_team.id
            ),
        }

        return data

    def __result_to_row(self, result: Result) -> dict:
        match_data = result.match_data
        match_stats = match_data.stats
        home_team = match_data.home_team
        away_team = match_data.away_team

        date = pd.to_datetime(datetime.utcfromtimestamp(result.date_time), format='%Y-%m-%dT%H:%M:%S')

        home_previous_results = self.__get_previous_results(date, home_team.id, 40)
        away_previous_results = self.__get_previous_results(date, away_team.id, 40)

        data = {
            'matchID': result.id,
            'round': result.round.name,
            'date': date,
            'season': result.season.name,
            'homeTeam': home_team.name,
            'homeGoals': self.__get_value('home_score', match_stats),
            'homeAvgScored': calculator.average_goals_scored_by_home_team(home_previous_results, home_team.id),
            'homeAvgConceded': calculator.average_goals_conceded_by_home_team(home_previous_results, home_team.id),
            'awayTeam': away_team.name,
            'awayGoals': self.__get_value('away_score', match_stats),
            'awayAvgScored': calculator.average_goals_scored_by_away_team(away_previous_results, away_team.id),
            'awayAvgConceded': calculator.average_goals_conceded_by_away_team(away_previous_results, away_team.id),
        }

        return data

    def __get_historical_results(
        self,
        date_before: datetime,
        home_team_id: int,
        away_team_id: int,
        limit: int
    ):
        results = self.result_client.get_historical_results_for_fixture(
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            date_before=date_before.strftime('%Y-%m-%dT%H:%M:%S+00:00'),
            limit=limit
        )

        return results[0:limit]

    def __get_previous_results(self, date_before: datetime, team_id: int, limit: int):
        results = self.result_client.get_results_for_team(
            team_id=team_id,
            limit=limit,
            date_before=date_before.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        )

        return results[0:limit]

    @staticmethod
    def __get_value(prop: str, stats: TeamStats):
        if stats.HasField(prop):
            p = getattr(stats, prop)
            return p.value

        return
