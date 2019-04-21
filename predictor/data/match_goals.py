from predictor.grpc.result_client import ResultClient
from datetime import datetime, date, time
import pandas as pd


class MatchGoalsAggregrator(object):
    def RecentForm(self, team_id, limit):
        today_beginning = datetime.combine(date.today(), time())

        now = today_beginning.astimezone()

        results = []

        for res in ResultClient().GetResultsForTeam(
                team_id=team_id,
                limit=limit,
                date_before=now.isoformat()
        ):
            results.append(self.__resultToRow(res))

        df = pd.DataFrame(results)

        return df

    @staticmethod
    def __resultToRow(result):
        match = result.match_data
        stats = match.stats
        d = {
            'Match_ID': result.id,
            'Home Team ID': match.home_team.id,
            'Home Goals Scored': stats.home_score.value,
            'Away Team ID': match.away_team.id,
            'Away Goals Scored': stats.away_score.value,
            'Home League Position': stats.home_league_position.value,
            'Away League Position': stats.away_league_position.value,
            'Date': result.date_time,
            'Is Cup': result.competition.is_cup.value,
            'Is Current Season': result.season.is_current.value,
            'Season ID': result.season.id,
        }
        return d
