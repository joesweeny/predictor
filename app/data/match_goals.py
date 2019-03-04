from app.grpc.client import result_client
from datetime import datetime, date, time


class MatchGoalsAggregrator:
    def RecentForm(self, team_id, limit):
        client = result_client.ResultClient()

        today_beginning = datetime.combine(date.today(), time())

        now = today_beginning.astimezone()

        results = []

        for res in client.GetResultsForTeam(team_id=team_id, limit=limit, date_before=now.isoformat()):
            results.append(res)

        for result in results:
            print(result)

        return len(results)
