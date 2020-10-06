from compiler.data_handling.goals import GoalsDataHandler
from compiler.models.odds import Odds
from tensorflow.keras.models import load_model
from typing import List


class OverUnderGoalsModel:
    def __init__(self, handler: GoalsDataHandler):
        self.__handler = handler
        self.__model = load_model('./assets/over_under_goals.h5')

    def get_odds(self, fixture_id: int) -> List[Odds]:
        fixture = self.__handler.get_match_goals_data_for_fixture(fixture_id=fixture_id)

        prediction = self.__model.predict(x=fixture.reshape(1, 1, 1))

        selection = prediction.reshape(-1)

        return self.__convert_odds(selection)

    @staticmethod
    def __convert_odds(prediction: float):
        if prediction > 0.50:
            over_price = round((1 / prediction), 2)
            under_price = round((1 / (1 - prediction)), 2)
        else:
            prediction = 1 - prediction
            over_price = round((1 / prediction), 2)
            under_price = round((1 / (1 - prediction)), 2)

        over = Odds(price=over_price, selection='over')
        under = Odds(price=under_price, selection='under')

        return [over, under]
