from typing import List, Tuple
import pandas as pd
from predictor.data.preprocessing import helpers
from predictor.data.aggregator.match_goals import MatchGoals
from predictor.data.repository.redis import RedisRepository
from predictor.grpc.proto.fixture.fixture_pb2 import Fixture


class MatchGoalsPreProcessor:
    def __init__(self, aggregator: MatchGoals, repository: RedisRepository):
        self.__aggregator = aggregator
        self.__repository = repository

    def pre_process_data_for_fixture(self, fixture: Fixture) -> Tuple[pd.DataFrame, pd.DataFrame]:
        fixture_df = self.__aggregator.for_fixture(fixture=fixture)

        features = self.__get_feature_data_frames(fixture.competition.id)

        features_df = self.__prepared_feature_data(features)

        features_df, fixture_df = self.__assign_elos(features=features_df, fixture=fixture_df)

        fixture_df = self.__calculate_rolling_averages(features=features_df, fixture=fixture_df, limit=160)

        features_df = helpers.create_target_variable_column(features_df)

        train_features = helpers.drop_non_features(features_df)

        predict_df = helpers.drop_non_features(fixture_df)

        train_features = train_features.astype(float)

        predict_df = predict_df.astype(float)

        return train_features, predict_df

    def __get_feature_data_frames(self, competition_id: int) -> List[pd.DataFrame]:
        dfs = self.__repository.get_data_frames_for_competition(competition_id=competition_id)

        if not dfs:
            raise FileExistsError('Unable to retrieve feature data frames for competition {}'.format(competition_id))

        return dfs

    @staticmethod
    def __prepared_feature_data(features: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Join all feature data frames into one data frame, sort by date and convert string formation data into
        corresponding integer mapping. Finish by filling any missing data with their column mean value
        """
        features_df = helpers.append_and_sort(features)

        features_df = helpers.map_formations(features_df)

        features_df.fillna(features_df.mean(), inplace=True)

        return features_df

    @staticmethod
    def __assign_elos(features: pd.DataFrame, fixture: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Calculate ELO ratings based on historic results and assign ratings to features and fixture data frames
        """
        elos, elo_probs, elos_current = helpers.elo_calculator(
            df=features,
            k_factor=25,
            historic_elos={team: 1500 for team in features['homeTeam'].unique()},
            soft_reset_factor=0.96,
            match_id_column='matchID'
        )

        features_df = helpers.apply_historic_elos(features, elos, elo_probs)

        fixture_df = helpers.apply_current_elos(fixture, elos_current, elo_probs)

        return features_df, fixture_df

    def __calculate_rolling_averages(self, features: pd.DataFrame, fixture: pd.DataFrame, limit: int) -> pd.DataFrame:
        """
        Parse last 10 weeks fixtures (approx 5 home and 5 away fixtures per team) an missing feature data
        in fixture data frame using exponential moving averages from recent fixtures
        """
        recent_fixtures = features[-limit:]

        combined_df = recent_fixtures.append(fixture)

        combined_df = helpers.set_unknown_features(combined_df, 5)

        row = combined_df[-1:]
        check = combined_df[-1:]

        check = check.drop(['homeGoals', 'awayGoals'], axis=1)

        if len(check.columns[check.isna().any()].tolist()) > 0:
            row = self.__calculate_rolling_averages(features, fixture, limit + limit)

        return row
