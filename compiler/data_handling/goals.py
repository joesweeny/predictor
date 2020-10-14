from datetime import datetime, timezone
from compiler.cache.redis import RedisRepository
from compiler.preprocessing.aggregation.goals import GoalsAggregator
from compiler.preprocessing.feature_creation.goals import process_fixture_data
from compiler.grpc.proto.fixture_pb2 import Fixture
import pandas as pd
import numpy as np
from typing import List


class GoalsDataHandler:
    def __init__(
        self,
        competitions: List,
        repository: RedisRepository,
        aggregator: GoalsAggregator
    ):
        self.__competitions = competitions
        self._repository = repository
        self._aggregator = aggregator

    def get_match_goals_data_for_fixture(self, fixture_id: int) -> (Fixture, np.array):
        fixture, fixture_data = self._aggregator.for_fixture(fixture_id=fixture_id)

        data = self.get_stored_match_goals_data_for_competition(competition_id=fixture.competition.id)

        return fixture, process_fixture_data(fixture=fixture_data.iloc[0], results=data)

    def get_stored_match_goals_data_for_competition(self, competition_id: int) -> pd.DataFrame:
        filename = "competition:" + str(competition_id) + ':goals'

        data = self._repository.get_data_frame(key=filename)

        if data is not None:
            return data

        for competition in self.__competitions:
            if competition['id'] == competition_id:
                df = self.__process_competition_season_data(
                    seasons=competition['seasons'],
                    competition_id=competition_id,
                    date_before=datetime.now(timezone.utc).replace(microsecond=0)
                )

                return df

        raise FileNotFoundError("Match Goal data for competition" + str(competition_id) + "does not exist")

    def store_match_goals_data_for_supported_competitions(self, date_before: datetime):
        """
        Loop through supported competitions and
            a) parse data into dataframe
            b) store dataframe to persistence layer
        """
        for competition in self.__competitions:
            competition_id = competition['id']
            seasons = competition['seasons']

            self.__process_competition_season_data(
                seasons=seasons,
                competition_id=competition_id,
                date_before=date_before
            )

    def __process_competition_season_data(
        self,
        seasons: List,
        competition_id: int,
        date_before: datetime
    ) -> pd.DataFrame:
        data_frame = pd.DataFrame()

        for season in seasons:
            df = self._aggregator.for_season(
                season_id=season['id'],
                date_before=date_before
            )

            data_frame = data_frame.append(other=df, ignore_index=True)

        filename = "competition:" + str(competition_id) + ':goals'

        self._repository.save_data_frame(key=filename, df=data_frame)

        return data_frame
