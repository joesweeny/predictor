import pandas as pd


def calculate_over_probability(row: pd.Series, df: pd.DataFrame, goals: int) -> float:
    """
    Calculate probability of fixture being over goals provided as third argument for a
    given row using the data frame provided as historical training data

    :param row pd.Series
    :param df  pd.DataFrame
    :param goals int
    :return float
    """
    home_filter = (df['homePosition'] <= row['homePosition']) & (df['homePosDiff'] <= row['homePosDiff'])
    away_filter = (df['awayPosition'] <= row['awayPosition']) & (df['awayPosDiff'] <= row['awayPosDiff'])

    filtered = df[home_filter & away_filter]
    over = filtered[filtered['totalGoals'] > goals]

    return round(len(over) / len(filtered), 2)
