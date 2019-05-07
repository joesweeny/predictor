import pandas as pd
from datetime import datetime
from predictor.grpc.result_client import ResultClient
from predictor.grpc.proto.result.result_pb2 import Result
from predictor.grpc.team_stats_client import TeamStatsClient
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
        'Home Goals',
        'Home Shots Total',
        'Home Shots On Goal',
        'Home Shots Off Goal',
        'Home Shots Inside Box',
        'Home Shots Outside Box',
        'Home Fouls',
        'Home Corners',
        'Home Saves',
        'Home Possession',
        'Home Yellow Cards',
        'Home Red Cards',
        'Home Pass Total',
        'Home Pass Accuracy',
        'Home Pass Percentage',
        'Home Offsides',
        'Away Team ID',
        'Away Team Name',
        'Away Days Since Last Match',
        'Away Formation',
        'Away Avg Goals Scored Last 5',
        'Away Avg Goals Conceded Last 5',
        'Away Goals',
        'Away Shots Total',
        'Away Shots On Goal',
        'Away Shots Off Goal',
        'Away Shots Inside Box',
        'Away Shots Outside Box',
        'Away Fouls',
        'Away Corners',
        'Away Saves',
        'Away Possession',
        'Away Yellow Cards',
        'Away Red Cards',
        'Away Pass Total',
        'Away Pass Accuracy',
        'Away Pass Percentage',
        'Away Offsides',
    ]

    def for_season(self, season_id: int) -> pd.DataFrame:
        df = pd.DataFrame(columns=self.__columns)

        for result in self.result_client.GetResultsForSeason(season_id):
            df = df.append(self.__resultToRow(result), ignore_index=True)

        return df

    def __resultToRow(self, result: Result) -> dict:
        competition = result.competition
        season = result.season
        match_data = result.match_data
        match_stats = match_data.stats
        home_team = match_data.home_team
        away_team = match_data.away_team

        home_previous_results = self.__getPreviousResults(result, home_team.id, 10)
        away_previous_results = self.__getPreviousResults(result, away_team.id, 10)

        historical_results = self.__getHistoricalResults(result, 10)

        data = {
            'Match ID': result.id,
            'Home Team ID': home_team.id,
            'Home Team Name': home_team.name,
            'Away Team ID': away_team.id,
            'Away Team Name': away_team.name,
            'Competition ID': competition.id,
            'Round': result.round.name,
            'Is Cup': competition.is_cup.value,
            'Season ID': season.id,
            'Is Current Season': season.is_current.value,
            'Referee ID': result.referee_id.value,
            'Venue ID': result.venue.id.value,
            'Date': result.date_time,
            'Home Days Since Last Match': calculator.DaysBetweenResults(
                result,
                home_previous_results[0],
            ),
            'Away Days Since Last Match': calculator.DaysBetweenResults(
                result,
                away_previous_results[0]
            ),
            'Home League Position': match_stats.home_league_position.value,
            'Away League Position': match_stats.away_league_position.value,
            'Home Formation': match_stats.home_formation.value,
            'Away Formation': match_stats.away_formation.value,
            'Home Goals Scored Last Match': calculator.GoalsScoredInMatch(
                home_previous_results[0],
                home_team.id
            ),
            'Home Goals Conceded Last Match': calculator.GoalsConcededInMatch(
                home_previous_results[0],
                home_team.id
            ),
            'Away Goals Scored Last Match': calculator.GoalsScoredInMatch(
                away_previous_results[0],
                away_team.id
            ),
            'Away Goals Conceded Last Match': calculator.GoalsConcededInMatch(
                away_previous_results[0],
                away_team.id
            ),
            'Home Avg Goals Scored Last 10': calculator.AverageGoalsScoredByTeam(
                home_previous_results,
                home_team.id
            ),
            'Home Avg Goals Conceded Last 10': calculator.AverageGoalsConcededByTeam(
                home_previous_results,
                home_team.id
            ),
            'Away Avg Goals Scored Last 10': calculator.AverageGoalsScoredByTeam(
                away_previous_results,
                away_team.id
            ),
            'Away Avg Goals Conceded Last 10': calculator.AverageGoalsConcededByTeam(
                away_previous_results,
                away_team.id
            ),
            'Average Goals for Fixture': calculator.AverageGoalsForResults(
                historical_results
            ),
            'Total Goals in Match': calculator.TotalGoalsForMatch(match_stats),
        }

        return data

    def __getHistoricalResults(self, current_result: Result, limit: int):
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

    def __getPreviousResults(self, current_result: Result, team_id: int, limit: int):
        date = datetime.utcfromtimestamp(current_result.date_time).astimezone()

        results = self.result_client.GetResultsForTeam(
            team_id=team_id,
            limit=limit,
            date_before=date.isoformat()
        )

        return results[0:limit]
