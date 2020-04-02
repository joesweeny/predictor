import pandas as pd
from typing import List
from compiler.models.total_goals.odds import Odds


def calculate_odds(row: pd.Series, df: pd.DataFrame, goals: int) -> List[Odds]:
    """
    Calculate odds for a given row using the data frame provided as historical training data

    :param row
    :param df
    :param goals
    :return List[Odds]
    """
    home_filter = (df['homePosition'] <= row['homePosition']) & (df['homePosDiff'] <= row['homePosDiff'])
    away_filter = (df['awayPosition'] <= row['awayPosition']) & (df['awayPosDiff'] <= row['awayPosDiff'])

    filtered = df[home_filter & away_filter]
    over = filtered[filtered['totalGoals'] > goals]

    probability = len(over) / len(filtered)

    return __parse_odds(probability)


def __parse_odds(probability: float) -> List[Odds]:
    over = Odds(price=(1 / probability), selection='OVER')
    under = Odds(price=(1 / (1 - probability)), selection="UNDER")

    return [over, under]
