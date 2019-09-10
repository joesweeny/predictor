from compiler.data.aggregator.match_goals import MatchGoals
from compiler.data.repository.redis import RedisRepository
from compiler.framework import config
from compiler.grpc.proto.fixture.fixture_pb2 import Fixture
import pandas as pd
from typing import List
from compiler.data.calculation import elo, stats
from compiler.data.preprocessing import helpers


STRENGTH_RATING_FACTOR = 50
MATCH_LIMIT = 3


def pre_process_historic_data_set(results: pd.DataFrame) -> pd.DataFrame:
    updated = helpers.apply_historic_elo_ratings(
        df=results,
        historic_elos={team: 1500 for team in results['homeTeam'].unique()},
        soft_reset_factor=0.96,
        goal_points=20
    )

    for index, row in updated.iterrows():
        __apply_shot_save_ratios_to_row(row=row, df=updated, index=index)
        __apply_goal_averages_to_row(row=row, df=updated, index=index)

    cleaned = updated.fillna(updated.mean()).round(2)

    return cleaned


def __apply_shot_save_ratios_to_row(row: pd.Series, df: pd.DataFrame, index: int):
    df.loc[index, 'homeShotTargetRatio'] = __apply_feature_ratio(row, 'homeShotsTotal', 'homeShotsOnGoal')
    df.loc[index, 'homeShotSaveRatio'] = __apply_feature_ratio(row, 'awayShotsOnGoal', 'homeSaves')
    df.loc[index, 'awayShotTargetRatio'] = __apply_feature_ratio(row, 'awayShotsTotal', 'awayShotsOnGoal')
    df.loc[index, 'awayShotSaveRatio'] = __apply_feature_ratio(row, 'homeShotsOnGoal', 'awaySaves')


def __apply_goal_averages_to_row(row: pd.Series, df: pd.DataFrame, index: int):
    df.loc[index, 'homeAvgScored'] = stats.calculate_feature_ratio(
        df,
        row,
        'homeTeam',
        'homeGoals',
        'awayDefenceStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'homeAvgConceded'] = stats.calculate_feature_ratio(
        df,
        row,
        'homeTeam',
        'awayGoals',
        'awayAttackStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'awayAvgScored'] = stats.calculate_feature_ratio(
        df,
        row,
        'awayTeam',
        'awayGoals',
        'homeDefenceStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )
    df.loc[index, 'awayAvgConceded'] = stats.calculate_feature_ratio(
        df,
        row,
        'awayTeam',
        'homeGoals',
        'homeAttackStrength',
        STRENGTH_RATING_FACTOR,
        MATCH_LIMIT
    )


def __apply_feature_ratio(row: pd.Series, col_1: str, col_2: str) -> float:
    return 0 if row[col_1] == 0 else row[col_2] / row[col_1]
