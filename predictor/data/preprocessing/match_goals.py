from typing import List, Tuple
from datetime import datetime, timezone
import pandas as pd
from predictor.data.preprocessing import helpers
from predictor.data.aggregator.match_goals import MatchGoals
from predictor.data.repository.redis import RedisRepository
from predictor.grpc.proto.fixture.fixture_pb2 import Fixture
from predictor.framework import config
from predictor.framework.exception import DataPreProcessingException


class MatchGoalsPreProcessor:
    __key = "match-goals:competition:{}"

    def __init__(self, aggregator: MatchGoals, repository: RedisRepository, configuration: config):
        self.__aggregator = aggregator
        self.__repository = repository
        self.__configuration = configuration

    def get_fixture_and_training_data_for_fixture(
        self,
        fixture: Fixture,
        goals: float
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Get pre processed current fixture and historic fixtures data frames to be used in predictive model
        """
        fixture_df = self.__aggregator.for_fixture(fixture=fixture)

        features_df = self.__repository.get_data_frame(key=self.__key.format(fixture.competition.id))

        if features_df is None:
            features_df = self.pre_process_feature_data_for_competition(competition_id=fixture.competition.id)

        return self.pre_process_feature_data_for_fixture(current=fixture_df, historic=features_df, goals=goals)

    def pre_process_feature_data_for_fixture(
        self,
        historic: pd.DataFrame,
        current: pd.DataFrame,
        goals: float
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Using current fixture and historic fixtures data frames create additional feature data and
        return two model ready data frames
        """
        features_df, fixture_df = self.__assign_elos(historic=historic, current=current)

        features_df = helpers.create_over_goals_target_variable_column(df=features_df, goals=goals)

        fixture_df = self.__calculate_rolling_averages(historic=features_df, current=fixture_df, limit=160)

        train_features = helpers.drop_non_features(df=features_df)

        predict_df = helpers.drop_non_features(df=fixture_df)

        return train_features.astype(float), predict_df.astype(float)

    def pre_process_feature_data_for_competition(self, competition_id: int) -> pd.DataFrame:
        """
        If competition provided is supported, aggregate and pre process feature data for
        supported seasons before persisting to cache database
        """
        data_frames = []

        competitions = self.__configuration.SUPPORTED_COMPETITIONS

        for i, competition in competitions.items():
            if competition['id'] == competition_id:
                seasons = competition['seasons']

                for season in seasons:
                    df = self.__aggregator.for_season(
                        season_id=season['id'],
                        date_before=datetime.now(timezone.utc).replace(microsecond=0)
                    )

                    data_frames.append(df)

        if not data_frames:
            raise DataPreProcessingException('Unable to pre process data for Competition {}'.format(competition_id))

        prepared = self.__prepare_feature_data(historic=data_frames)

        self.__repository.save_data_frame(df=prepared, key=self.__key.format(competition_id))

        return prepared

    @staticmethod
    def __prepare_feature_data(historic: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Join all feature data frames into one data frame, sort by date and convert string formation data into
        corresponding integer mapping. Finish by filling any missing data with their column mean value
        """
        features_df = helpers.append_and_sort_by_column(dfs=historic, col='date', asc=True)

        features_df = helpers.map_formations(features_df)

        features_df.fillna(features_df.mean(), inplace=True)

        return features_df

    @staticmethod
    def __assign_elos(historic: pd.DataFrame, current: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Calculate ELO ratings based on historic results and assign ratings to features and fixture data frames
        """
        elos, elo_probs, elos_current = helpers.elo_calculator(
            df=historic,
            k_factor=25,
            historic_elos={team: 1500 for team in historic['homeTeam'].unique()},
            soft_reset_factor=0.96,
            match_id_column='matchID'
        )

        features_df = helpers.apply_historic_elos(historic, elos, elo_probs)

        fixture_df = helpers.apply_current_elos(current, elos_current)

        return features_df, fixture_df

    def __calculate_rolling_averages(self, historic: pd.DataFrame, current: pd.DataFrame, limit: int) -> pd.DataFrame:
        """
        Parse historic fixtures (based on limit provided) and calculate missing feature data
        in current fixture data frame using exponential moving averages from recent fixtures
        """
        recent_fixtures = historic[-limit:]

        combined_df = recent_fixtures.append(current)

        combined_df = helpers.set_unknown_features(combined_df, 5)

        row = combined_df[-1:]
        check = combined_df[-1:]

        check = check.drop(['homeGoals', 'awayGoals'], axis=1)

        if len(check.columns[check.isna().any()].tolist()) > 0:
            row = self.__calculate_rolling_averages(historic, current, limit + 20)

        return row
