import pandas as pd
from datetime import datetime
from predictor.grpc.result_client import ResultClient
from predictor.grpc.proto.result.result_pb2 import Result
from predictor.data import calculator


class MatchGoals:
    def __init__(self, client: ResultClient):
        self.result_client = client

    __columns = [
        'Match ID',
        'Home Team ID',
        'Home Team Name',
        'Away Team ID',
        'Away Team Name',
        'Competition ID',
        'Round',
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
        'Average Goals for Fixture',
        'Total Goals in Match',
    ]

    def ForSeason(self, season_id: int) -> pd.DataFrame:
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

        home_previous_results = self.__getPreviousResults(result, home_team.id, 20)
        away_previous_results = self.__getPreviousResults(result, away_team.id, 20)

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
            'Home Avg Goals Scored Last 20': calculator.AverageGoalsScoredByTeam(
                home_previous_results,
                home_team.id
            ),
            'Home Avg Goals Conceded Last 20': calculator.AverageGoalsConcededByTeam(
                home_previous_results,
                home_team.id
            ),
            'Away Avg Goals Scored Last 20': calculator.AverageGoalsScoredByTeam(
                away_previous_results,
                away_team.id
            ),
            'Away Avg Goals Conceded Last 20': calculator.AverageGoalsConcededByTeam(
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
