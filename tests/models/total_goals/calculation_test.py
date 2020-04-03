import pandas as pd
from compiler.models.total_goals.calculation import calculate_over_probability
from compiler.models.total_goals import feature_creation
from compiler.models.total_goals import preprocessing


def test_calculate_over_probability_returns_a_probability_calculation_float():
    df = pd.read_csv("/opt/tests/test-data/premier-league-2014-2020.csv")
    df = df[['season', 'round', 'homeTeam', 'awayTeam', 'totalGoals']]

    stats = feature_creation.calculate_round_goal_stats(df)
    tables = feature_creation.convert_to_league_positions(stats)
    prepped = preprocessing.prepare_dataframe(df, tables)

    row = prepped.iloc[-1]
    df = prepped[:-1]

    prob = calculate_over_probability(row, df, 2)

    assert prob == 0.58
