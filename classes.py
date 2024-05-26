class Card:
    def __init__(self, name: str, value: int) -> None:
        self._name = name
        self._value = value
        pass

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> int:
        return self._value


class Ace(Card):
    def min_value(self) -> int:
        self._value = 1
        return self._value

    def max_value(self) -> int:
        self._value = 10
        return self._value
