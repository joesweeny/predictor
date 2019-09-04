import pandas as pd


def add_average_goals_features(df: pd.Dataframe) -> pd.Dataframe:
    for index, row in df.iterrows():
        rows_before = df.iloc[0:index]

        home_rows = rows_before[rows_before['homeTeam'] == row['homeTeam']]
        away_rows = rows_before[rows_before['awayTeam'] == row['awayTeam']]

        if home_rows['homeTeam'].count() == 0 or away_rows['awayTeam'].count() == 0:
            df.loc[index, 'homeAvgScored'] = row['homeGoals']
            df.loc[index, 'homeAvgConceded'] = row['awayGoals']
            df.loc[index, 'awayAvgScored'] = row['awayGoals']
            df.loc[index, 'awayAvgConceded'] = row['homeGoals']
            continue

        df.loc[index, 'homeAvgScored'] = home_rows['homeGoals'].mean()
        df.loc[index, 'homeAvgConceded'] = home_rows['awayGoals'].mean()

        df.loc[index, 'awayAvgScored'] = away_rows['awayGoals'].mean()
        df.loc[index, 'awayAvgConceded'] = away_rows['homeGoals'].mean()

    return df


def add_shot_ratio_features(df: pd.Dataframe) -> pd.Dataframe:
    for index, row in df.iterrows():
        seasons[index, 'homeShotTargetRatio'] = __parse_feature(row, 'homeShotsTotal', 'homeShotsOnGoal')
        seasons.loc[index, 'homeShotSaveRatio'] = __parse_feature(row, 'awayShotsOnGoal', 'homeSaves')
        seasons.loc[index, 'awayShotTargetRatio'] = __parse_feature(row, 'awayShotsTotal', 'awayShotsOnGoal')
        seasons.loc[index, 'awayShotSaveRatio'] = __parse_feature(row, 'homeShotsOnGoal', 'awaySaves')

    return df


def __parse_feature(row: pd.Series, col_1: str, col_2: str) -> int:
    return 0 if row[col_1] == 0 else row[col_2] / row[col_1]
