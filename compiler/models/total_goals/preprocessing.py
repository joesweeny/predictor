import pandas as pd
from typing import Dict


def prepare_dataframe(df: pd.DataFrame, stats: Dict) -> pd.DataFrame:
    """
    Prepare data frame by adding stats provided to data frame and removing rows containing
    null value columns

    :param df pd.DataFrame
    :param stats Dict
    :return pd.DataFrame
    """
    for index, row in df.iterrows():
        if row['round'] == 1:
            continue

        home_pos, home_goals, home_diff = __get_team_stats(stats, row['season'], row['round'], row['homeTeam'])
        away_pos, away_goals, away_diff = __get_team_stats(stats, row['season'], row['round'], row['awayTeam'])

        df.loc[index, 'homePosition'] = home_pos
        df.loc[index, 'homePosDiff'] = home_diff

        df.loc[index, 'awayPosition'] = away_pos
        df.loc[index, 'awayPosDiff'] = away_diff

    df = df.dropna()

    return df


def __get_team_stats(stats, season, r, team):
    parsed_round = stats[season][r]

    for elem in parsed_round:
        if elem['team'] == team:
            return elem['position'], elem['goals'], elem['diff']

    return None, None, None
