import pandas as pd


class MatchGoals:
    __columns = [
        'Match_ID',
        'Competition ID',
        'Season ID',
        'Referee ID',
        'Venue ID',
        'Is Cup',
        'Is Current Season',
        'Date',
        'Days Since Last Match',
        'Home Team ID',
        'Away Team ID',
        'Home League Position',
        'Away League Position',
        'Home Formation',
        'Away Formation',
        'Home Avg Goals Scored Last 20',
        'Away Avg Goals Conceded Last 20',
        'Home Goals in Lineup',
        'Away Goals in Lineup',
        'Average Goals in Fixture',
        'Total Goals in Match',
    ]

    def ForSeason(self):
        df = pd.DataFrame(columns=self.__columns)

        return df
