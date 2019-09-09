from compiler.data.aggregator.match_goals import MatchGoals
from compiler.data.repository.redis import RedisRepository
from compiler.framework import config
from compiler.grpc.proto.fixture.fixture_pb2 import Fixture
import pandas as pd
from typing import List
from compiler.data.calculation import elo, stats


def pre_process_historic_data_set(results: pd.DataFrame) -> pd.DataFrame:
    # Add team strength columns
    updated = helpers.apply_historic_elo_ratings(
        df=results,
        historic_elos={team: 1500 for team in results['homeTeam'].unique()},
        soft_reset_factor=0.96,
        goal_points=20
    )

    # Add ratio columns
    for index, row in updated.iterrows():
        updated.loc[index, 'homeShotTargetRatio'] = __apply_feature_ratio(row, 'homeShotsTotal', 'homeShotsOnGoal')
        updated.loc[index, 'homeShotSaveRatio'] = __apply_feature_ratio(row, 'awayShotsOnGoal', 'homeSaves')
        updated.loc[index, 'awayShotTargetRatio'] = __apply_feature_ratio(row, 'awayShotsOnGoal', 'awayShotsTotal')
        updated.loc[index, 'awayShotSaveRatio'] = __apply_feature_ratio(row, 'homeShotsOnGoal', 'awaySaves')

    updated = updated.fillna(seasons.mean())
    updated = updated.round(2)

    # Add average scored columns

    # return data frame
    return updated


def __apply_feature_ratio(row: pd.Series, col_1: str, col_2: str) -> float:
    return 0 if row[col_1] == 0 else row[col_2] / row[col_1]
