from compiler.data.aggregator.match_goals import MatchGoals
from compiler.data.repository.redis import RedisRepository
from compiler.framework import config
from compiler.grpc.proto.fixture.fixture_pb2 import Fixture
import pandas as pd
from typing import List
from compiler.data.calculation import elo, stats



def pre_process_historic_data_set(self, results: pd.DataFrame) -> pd.DataFrame:
# Add team strength columns

# Add ratio columns

# Add average scored columns

# return data frame