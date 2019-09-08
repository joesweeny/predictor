import pandas as pd


def calculate_feature_ratio(
    df: pd.DataFrame,
    team: str,
    row: pd.Series,
    feature: str,
    rating: float,
    factor: int,
    row_count: int
) -> float:
    """
    Calculate the ratio of a given column based from parsed columns based on
    rating parameter provided i.e. calculate shot to goal ratio for a team based
    on similar rated teams to the opposition
    :param df:
    :param team:
    :param row:
    :param feature:
    :param rating:
    :param factor:
    :param row_count:
    :return:
    """
    elo = row[rating]

    home_rows = df[df[team] == row[team]]

    parsed = __parse_rows(home_rows, column, elo, factor)

    if parsed.shape[0] == 0:
        parsed = home_rows

    parsed = parsed.iloc[row_count:]

    return round(parsed[feature].mean(), 2)


def __parse_rows(rows, column, elo, factor):
    return rows.loc[(rows[column] <= (elo + factor))]
