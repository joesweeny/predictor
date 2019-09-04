class OverUnderGoals:
    def __init__(self, under: float, over: float):
        self.__under = under
        self.__over = over

    def get_under_decimal_odds(self) -> float:
        return self.__under

    def get_over_decimal_odds(self) -> float:
        return self.__over
