class Odds:
    def __init__(self, price: float, selection: str):
        self.__price = price
        self.__selection = selection

    def get_price(self) -> float:
        return self.__price

    def get_selection(self) -> str:
        return self.__selection
