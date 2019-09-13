import pandas as pd


def calculate_feature_ratio(
    df: pd.DataFrame,
    row: pd.Series,
    home_away: str,
    feature: str,
    rating: str,
    factor: int,
    row_count: int
) -> float:
    """
    Calculate the ratio of a given feature column, parsing columns based on
    rating parameter provided i.e. calculate shot to goal ratio for a team based
    on similar rated opposition teams

    :param df: Pandas data frame of data
    :param row: Feature row
    :param home_away: homeTeam or awayTeam string
    :param feature: Feature name to calculate
    :param rating: Strength rating column to use i.e. homeAttackStrength
    :param factor: Range of opposition strength to allow for
    :param row_count: How many rows used to calculate ratio
    :return: Calculated ratio of feature
    """
    elo = row[rating]

    rows = df[df[home_away] == row[home_away]]

    parsed = __parse_rows(rows, rating, elo, factor)

    if parsed.shape[0] == 0:
        parsed = rows

    total = parsed.iloc[-row_count:]

    return round(total[feature].mean(), 2)


def calculate_home_advantage(row: pd.Series, df: pd.DataFrame, index: int) -> float:
    """
    Calculate a Home Teams home scoring ability and strength
    :param row:
    :param df:
    :param index:
    :return:
    """
    rows = df[df['season'] == row['season']]

    if index > 0:
        rows = rows.iloc[0:index-1]

    team_rows = rows[rows['homeTeam'] == row['homeTeam']]

    return team_rows['homeGoals'].sum() / team_rows['homeTeam'].count()


def __parse_rows(rows, rating, elo, factor):
    return rows.loc[(rows[rating] <= (elo + factor))]
