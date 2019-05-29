import pandas as pd
from datetime import datetime
from predictor.grpc.proto.fixture.fixture_pb2 import Fixture
from predictor.grpc.result_client import ResultClient
from predictor.grpc.proto.result.result_pb2 import Result
from predictor.grpc.team_stats_client import TeamStatsClient
from predictor.grpc.proto.stats.team.stats_pb2 import TeamStats
from predictor.data import calculator


class MatchGoals:
    def __init__(self, result_client: ResultClient, team_stats_client: TeamStatsClient):
        self.result_client = result_client
        self.team_stats_client = team_stats_client

    __columns = [
        'matchID',
        'round',
        'date',
        'season',
        'averageGoalsForFixture',
        'homeTeamID',
        'homeTeam',
        'homeDaysSinceLastMatch',
        'homeFormation',
        'homeAvgScoredLast5',
        'homeAvgConcededLast5',
        'homeScoredLastMatch',
        'homeConcededLastMatch',
        'homeShotsTotal',
        'homeShotsOnGoal',
        'homeShotsOffGoal',
        'homeShotsInsideBox',
        'homeShotsOutsideBox',
        'homeAttacksTotal',
        'homeAttacksDangerous',
        'homeGoals',
        'awayTeamID',
        'awayTeam',
        'awayDaysSinceLastMatch',
        'awayFormation',
        'awayAvgScoredLast5',
        'awayAvgConcededLast5',
        'awayScoredLastMatch',
        'awayConcededLastMatch',
        'awayShotsTotal',
        'awayShotsOnGoal',
        'awayShotsOffGoal',
        'awayShotsInsideBox',
        'awayShotsOutsideBox',
        'awayAttacksTotal',
        'awayAttacksDangerous',
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

    def __fixture_to_row(self, fixture: Fixture):
        home_team = fixture.home_team
        away_team = fixture.away_team

        date = datetime.utcfromtimestamp(fixture.date_time)

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
            'date': date.strftime('%Y-%m-%dT%H:%M:%S'),
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

        date = datetime.utcfromtimestamp(result.date_time)

        home_previous_results = self.__get_previous_results(date, home_team.id, 5)
        away_previous_results = self.__get_previous_results(date, away_team.id, 5)

        historical_results = self.__get_historical_results(
            date_before=date,
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            limit=10
        )

        stats = self.team_stats_client.get_team_stats_for_fixture(fixture_id=result.id)

        home_stats = stats.home_team
        away_stats = stats.away_team

        data = {
            'matchID': result.id,
            'round': result.round.name,
            'date': date.strftime('%Y-%m-%dT%H:%M:%S'),
            'season': result.season.name,
            'averageGoalsForFixture': calculator.AverageGoalsForResults(
                historical_results
            ),
            'homeTeamID': home_team.id,
            'homeTeam': home_team.name,
            'homeDaysSinceLastMatch': calculator.days_between_results(
                date,
                home_previous_results[0],
            ),
            'homeFormation': match_stats.home_formation.value,
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
            'homeShotsTotal': self.__get_value('shots_total', home_stats),
            'homeShotsOnGoal': self.__get_value('shots_on_goal', home_stats),
            'homeShotsOffGoal': self.__get_value('shots_off_goal', home_stats),
            'homeShotsInsideBox': self.__get_value('shots_inside_box', home_stats),
            'homeShotsOutsideBox': self.__get_value('shots_outside_box', home_stats),
            'homeAttacksTotal': self.__get_value('attacks_total', home_stats),
            'homeAttacksDangerous': self.__get_value('attacks_dangerous', home_stats),
            'homeGoals': self.__get_value('home_score', match_stats),
            'awayTeamID': away_team.id,
            'awayTeam': away_team.name,
            'awayDaysSinceLastMatch': calculator.days_between_results(
                date,
                away_previous_results[0]
            ),
            'awayFormation': match_stats.away_formation.value,
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
            'awayShotsTotal': self.__get_value('shots_total', away_stats),
            'awayShotsOnGoal': self.__get_value('shots_on_goal', away_stats),
            'awayShotsOffGoal': self.__get_value('shots_off_goal', away_stats),
            'awayShotsInsideBox': self.__get_value('shots_inside_box', away_stats),
            'awayShotsOutsideBox': self.__get_value('shots_outside_box', away_stats),
            'awayAttacksTotal': self.__get_value('attacks_total', away_stats),
            'awayAttacksDangerous': self.__get_value('attacks_dangerous', away_stats),
            'awayGoals': self.__get_value('away_score', match_stats),
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
