from datetime import datetime, timezone
from compiler.data.repository.redis import RedisRepository
from compiler.data.aggregator.match_goals import MatchGoals
from compiler.data.preprocessing.match_goals import pre_process_historic_data_set, pre_process_fixture_data
from compiler.framework import config
import pandas as pd
from typing import List


class DataHandler:
    def __init__(
        self,
        configuration: config,
        repository: RedisRepository,
        aggregator: MatchGoals
    ):
        self._configuration = configuration
        self._repository = repository
        self._aggregator = aggregator

    def get_match_goals_data_for_fixture(self, fixture_id: int) -> pd.DataFrame:
        filename = "fixture:" + str(fixture_id) + ':match_goals'

        data = self._repository.get_data_frame(key=filename)

        if data is not None:
            return data

        fixture, fixture_data = self._aggregator.for_fixture(fixture_id=fixture_id)

        data = self.get_stored_match_goals_data_for_competition(competition_id=fixture.competition.id)

        pre_processed = pre_process_fixture_data(fixture=fixture_data, results=data)

        self._repository.save_data_frame(key=filename, df=pre_processed)

        return pre_processed

    def get_stored_match_goals_data_for_competition(self, competition_id: int) -> pd.DataFrame:
        filename = "competition:" + str(competition_id) + ':match_goals'

        data = self._repository.get_data_frame(key=filename)

        if data is not None:
            return data

        competitions = self._configuration.SUPPORTED_COMPETITIONS

        for i, competition in competitions.items():
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
        competitions = self._configuration.SUPPORTED_COMPETITIONS

        for i, competition in competitions.items():
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

        pre_processed = pre_process_historic_data_set(results=data_frame)

        filename = "competition:" + str(competition_id) + ':match_goals'

        self._repository.save_data_frame(key=filename, df=pre_processed)

        return pre_processed
