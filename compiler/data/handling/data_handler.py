from datetime import datetime
from compiler.data.repository.redis import RedisRepository
from compiler.data.aggregator.match_goals import MatchGoals
from compiler.data.preprocessing.match_goals import pre_process_historic_data_set
from compiler.framework import config
import pandas as pd


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

            data_frame = pd.DataFrame()

            for season in seasons:
                df = self._aggregator.for_season(
                    season_id=season['id'],
                    date_before=date_before
                )

                data_frame = data_frame.append(other=df, ignore_index=True)

            pre_processed = pre_process_historic_data_set(results=data_frame)

            filename = "competition:" + str(competition_id) + ':match_goals.csv'

            self._repository.save_data_frame(key=filename, df=pre_processed)

    def get_stored_match_goals_data_for_competition(self, competition_id: int):
        filename = "competition:" + str(competition_id) + ':match_goals.csv'

        data = self._repository.get_data_frame(key=filename)

        if data is None:
            raise FileNotFoundError("Match Goal data for competition" + str(competition_id) + "does not exist")

        return data
