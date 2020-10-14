from compiler.data_handling.goals import GoalsDataHandler
from compiler.models.odds import Odds
from tensorflow.keras.models import model_from_json
from typing import List


class OverUnderGoalsModel:
    def __init__(self, handler: GoalsDataHandler, competitions: List):
        self.__handler = handler
        self.__competitions = competitions

    def get_odds(self, fixture_id: int) -> List[Odds]:
        fixture, fixture_row = self.__handler.get_match_goals_data_for_fixture(fixture_id=fixture_id)

        model = self.__load_model(fixture.competition.id)

        prediction = model.predict(x=fixture_row.reshape(fixture_row.shape[0], 1, fixture_row.shape[1]))

        selection = prediction.reshape(-1)

        return self.__convert_odds(selection[0])

    def __load_model(self, competition_id: int):
        for competition in self.__competitions:
            if competition['id'] == competition_id:
                filename = competition['model']
                return self.__build_model(filename)

        raise NotImplemented(f'Over under goals model not available for competition {competition_id}')

    @staticmethod
    def __build_model(filename: str):
        json_file = open(f'compiler/models/assets/{filename}.json', 'r')
        loaded_model = model_from_json(json_file.read())
        json_file.close()
        loaded_model.load_weights(f'compiler/models/assets/{filename}.h5')
        return loaded_model

    @staticmethod
    def __convert_odds(prediction: float):
        if prediction > 0.50:
            over_price = round((1 / prediction), 2)
            under_price = round((1 / (1 - prediction)), 2)
        else:
            prediction = 1 - prediction
            under_price = round((1 / prediction), 2)
            over_price = round((1 / (1 - prediction)), 2)

        over = Odds(price=over_price, selection='over')
        under = Odds(price=under_price, selection='under')

        return [over, under]
