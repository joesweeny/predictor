import pandas as pd
from compiler.data.calculation import stats
from compiler.data.preprocessing import helpers

GOAL_POINTS = 20
MATCH_LIMIT = 3
STRENGTH_RATING_FACTOR = 50


def pre_process_historic_data_set(results: pd.DataFrame) -> pd.DataFrame:
    updated = helpers.apply_historic_elo_ratings(
        df=results,
        historic_elos={team: 1500 for team in results['homeTeam'].unique()},
        soft_reset_factor=0.96,
        goal_points=GOAL_POINTS
    )

    updated = updated.fillna(updated.mean())

    for index, row in updated.iterrows():
        __apply_shot_save_ratios_to_row(row=row, df=updated, index=index)
        __apply_goal_averages_to_row(row=row, df=updated, index=index)
        __apply_home_advantage(row=row, df=updated, index=index)

    cleaned = updated.fillna(updated.mean()).round(2)

    return cleaned


def pre_process_fixture_data(fixture: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    updated = helpers.apply_current_elo_ratings_for_fixture(
        fixture=fixture,
        data=results,
        points=GOAL_POINTS
    )

    row = fixture.iloc[0, :]

    updated.loc[0, 'homeShotTargetRatio'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='homeTeam',
        feature='homeShotTargetRatio',
        rating='awayDefenceStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'homeShotSaveRatio'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='homeTeam',
        feature='homeShotSaveRatio',
        rating='awayAttackStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'awayShotTargetRatio'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='awayTeam',
        feature='awayShotTargetRatio',
        rating='homeDefenceStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'awayShotSaveRatio'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='awayTeam',
        feature='awayShotSaveRatio',
        rating='homeAttackStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'homeAvgScored'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='homeTeam',
        feature='homeGoals',
        rating='awayDefenceStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'homeAvgConceded'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='homeTeam',
        feature='awayGoals',
        rating='awayAttackStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'awayAvgScored'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='awayTeam',
        feature='awayGoals',
        rating='homeDefenceStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'awayAvgConceded'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='awayTeam',
        feature='homeGoals',
        rating='homeAttackStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'homeXGFor'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='homeTeam',
        feature='homeXG',
        rating='awayDefenceStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'homeXGAgainst'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='homeTeam',
        feature='awayXG',
        rating='awayAttackStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'awayXGFor'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='awayTeam',
        feature='awayXG',
        rating='homeDefenceStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'awayXGAgainst'] = stats.calculate_feature_average(
        df=results,
        row=row,
        home_away='awayTeam',
        feature='homeXG',
        rating='homeAttackStrength',
        factor=STRENGTH_RATING_FACTOR,
        row_count=MATCH_LIMIT
    )

    updated.loc[0, 'homeAdvantage'] = stats.calculate_home_advantage(
        row=row,
        df=results,
        index=0
    )

    return updated


def __apply_shot_save_ratios_to_row(row: pd.Series, df: pd.DataFrame, index: int):
    df.loc[index, 'homeShotTargetRatio'] = __apply_feature_ratio(row, 'homeShotsTotal', 'homeShotsOnGoal')
    df.loc[index, 'homeShotSaveRatio'] = __apply_feature_ratio(row, 'awayShotsOnGoal', 'homeSaves')
    df.loc[index, 'awayShotTargetRatio'] = __apply_feature_ratio(row, 'awayShotsTotal', 'awayShotsOnGoal')
    df.loc[index, 'awayShotSaveRatio'] = __apply_feature_ratio(row, 'homeShotsOnGoal', 'awaySaves')


def __apply_goal_averages_to_row(row: pd.Series, df: pd.DataFrame, index: int):
    df.loc[index, 'homeAvgScored'] = stats.calculate_feature_average(
        df,
        row,
        'homeTeam',
        'homeGoals',
        'awayDefenceStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'homeAvgConceded'] = stats.calculate_feature_average(
        df,
        row,
        'homeTeam',
        'awayGoals',
        'awayAttackStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'awayAvgScored'] = stats.calculate_feature_average(
        df,
        row,
        'awayTeam',
        'awayGoals',
        'homeDefenceStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'awayAvgConceded'] = stats.calculate_feature_average(
        df,
        row,
        'awayTeam',
        'homeGoals',
        'homeAttackStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'homeAvgScored'] = stats.calculate_feature_average(
        df,
        row,
        'homeTeam',
        'homeGoals',
        'awayDefenceStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'homeXGFor'] = stats.calculate_feature_average(
        df,
        row,
        'homeTeam',
        'homeXG',
        'awayDefenceStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'homeXGAgainst'] = stats.calculate_feature_average(
        df,
        row,
        'homeTeam',
        'awayXG',
        'awayAttackStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'awayXGFor'] = stats.calculate_feature_average(
        df,
        row,
        'awayTeam',
        'awayXG',
        'homeDefenceStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'awayXGAgainst'] = stats.calculate_feature_average(
        df,
        row,
        'awayTeam',
        'homeXG',
        'homeAttackStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )


def __apply_feature_ratio(row: pd.Series, col_1: str, col_2: str) -> float:
    return 0 if row[col_1] == 0 else row[col_2] / row[col_1]


def __apply_home_advantage(row: pd.Series, df: pd.DataFrame, index: int):
    df.loc[index, 'homeAdvantage'] = stats.calculate_home_advantage(row=row, df=df, index=index)
