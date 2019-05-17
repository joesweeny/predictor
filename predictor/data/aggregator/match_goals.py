import pandas as pd
from datetime import datetime
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
        'Match ID',
        'Round',
        'Referee ID',
        'Venue ID',
        'Date',
        'Average Goals for Fixture',
        'Home Team ID',
        'Home Team Name',
        'Home Days Since Last Match',
        'Home Formation',
        'Home Avg Goals Scored Last 5',
        'Home Avg Goals Conceded Last 5',
        'Home Goals Scored Last Match',
        'Home Goals Conceded Last Match',
        'Home Shots Total',
        'Home Shots On Goal',
        'Home Shots Off Goal',
        'Home Shots Inside Box',
        'Home Shots Outside Box',
        'Home Corners',
        'Home Possession',
        'Home Pass Total',
        'Home Pass Accuracy',
        'Home Pass Percentage',
        'Away Team ID',
        'Away Team Name',
        'Away Days Since Last Match',
        'Away Formation',
        'Away Avg Goals Scored Last 5',
        'Away Avg Goals Conceded Last 5',
        'Away Goals Scored Last Match',
        'Away Goals Conceded Last Match',
        'Away Shots Total',
        'Away Shots On Goal',
        'Away Shots Off Goal',
        'Away Shots Inside Box',
        'Away Shots Outside Box',
        'Away Corners',
        'Away Possession',
        'Away Pass Total',
        'Away Pass Accuracy',
        'Away Pass Percentage',
        'Total Goals in Match',
    ]

    def for_season(self, season_id: int) -> pd.DataFrame:
        df = pd.DataFrame(columns=self.__columns)

        for result in self.result_client.GetResultsForSeason(season_id):
            df = df.append(self.__result_to_row(result), ignore_index=True)

        return df

    def __result_to_row(self, result: Result) -> dict:
        match_data = result.match_data
        match_stats = match_data.stats
        home_team = match_data.home_team
        away_team = match_data.away_team

        home_previous_results = self.__get_previous_results(result, home_team.id, 5)
        away_previous_results = self.__get_previous_results(result, away_team.id, 5)

        historical_results = self.__get_historical_results(result, 10)

        stats = self.team_stats_client.get_team_stats_for_fixture(fixture_id=result.id)

        home_stats = stats.home_team
        away_stats = stats.away_team

        data = {
            'Match ID': result.id,
            'Round': result.round.name,
            'Referee ID': result.referee_id.value,
            'Venue ID': result.venue.id.value,
            'Date': result.date_time,
            'Average Goals for Fixture': calculator.AverageGoalsForResults(
                historical_results
            ),
            'Home Team ID': home_team.id,
            'Home Team Name': home_team.name,
            'Home Days Since Last Match': calculator.DaysBetweenResults(
                result,
                home_previous_results[0],
            ),
            'Home Formation': match_stats.home_formation.value,
            'Home Avg Goals Scored Last 5': calculator.AverageGoalsScoredByTeam(
                home_previous_results,
                home_team.id
            ),
            'Home Avg Goals Conceded Last 5': calculator.AverageGoalsConcededByTeam(
                home_previous_results,
                home_team.id
            ),
            'Home Goals Scored Last Match': calculator.GoalsScoredInMatch(
                home_previous_results[0],
                home_team.id
            ),
            'Home Goals Conceded Last Match': calculator.GoalsConcededInMatch(
                home_previous_results[0],
                home_team.id
            ),
            'Home Shots Total': self.__get_value('shots_total', home_stats),
            'Home Shots On Goal': self.__get_value('shots_on_goal', home_stats),
            'Home Shots Off Goal': self.__get_value('shots_off_goal', home_stats),
            'Home Shots Inside Box': self.__get_value('shots_inside_box', home_stats),
            'Home Shots Outside Box': self.__get_value('shots_outside_box', home_stats),
            'Home Corners': self.__get_value('corners', home_stats),
            'Home Possession': self.__get_value('possession', home_stats),
            'Home Pass Total': self.__get_value('passes_total', home_stats),
            'Home Pass Accuracy': self.__get_value('passes_accuracy', home_stats),
            'Home Pass Percentage': self.__get_value('passes_percentage', home_stats),
            'Away Team ID': away_team.id,
            'Away Team Name': away_team.name,
            'Away Days Since Last Match': calculator.DaysBetweenResults(
                result,
                away_previous_results[0]
            ),
            'Away Formation': match_stats.away_formation.value,
            'Away Avg Goals Scored Last 5': calculator.AverageGoalsScoredByTeam(
                away_previous_results,
                away_team.id
            ),
            'Away Avg Goals Conceded Last 5': calculator.AverageGoalsConcededByTeam(
                away_previous_results,
                away_team.id
            ),
            'Away Goals Scored Last Match': calculator.GoalsScoredInMatch(
                away_previous_results[0],
                away_team.id
            ),
            'Away Goals Conceded Last Match': calculator.GoalsConcededInMatch(
                away_previous_results[0],
                away_team.id
            ),
            'Away Shots Total': self.__get_value('shots_total', away_stats),
            'Away Shots On Goal': self.__get_value('shots_on_goal', away_stats),
            'Away Shots Off Goal': self.__get_value('shots_off_goal', away_stats),
            'Away Shots Inside Box': self.__get_value('shots_inside_box', away_stats),
            'Away Shots Outside Box': self.__get_value('shots_outside_box', away_stats),
            'Away Corners': self.__get_value('corners', away_stats),
            'Away Possession': self.__get_value('possession', away_stats),
            'Away Pass Total': self.__get_value('passes_total', away_stats),
            'Away Pass Accuracy': self.__get_value('passes_accuracy', away_stats),
            'Away Pass Percentage': self.__get_value('passes_percentage', away_stats),
            'Total Goals in Match': calculator.TotalGoalsForMatch(match_stats),
        }

        return data

    def __get_historical_results(self, current_result: Result, limit: int):
        date = datetime.utcfromtimestamp(current_result.date_time).astimezone()

        home_team = current_result.match_data.home_team
        away_team = current_result.match_data.away_team

        results = self.result_client.GetHistoricalResultsForFixture(
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            date_before=date.isoformat(),
            limit=limit
        )

        return results[0:limit]

    def __get_previous_results(self, current_result: Result, team_id: int, limit: int):
        date = datetime.utcfromtimestamp(current_result.date_time).astimezone()

        results = self.result_client.GetResultsForTeam(
            team_id=team_id,
            limit=limit,
            date_before=date.isoformat()
        )

        return results[0:limit]

    @staticmethod
    def __get_value(prop: str, stats: TeamStats):
        if stats.HasField(prop):
            p = getattr(stats, prop)
            return p.value

        return
