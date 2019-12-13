class OverUnderGoals:
    def __init__(self, model: str, under: float, over: float):
        self.__model = model
        self.__under = under
        self.__over = over

    def get_model_name(self) -> str:
        return self.__model

    def get_under_decimal_odds(self) -> float:
        return self.__under

    def get_over_decimal_odds(self) -> float:
        return self.__over
