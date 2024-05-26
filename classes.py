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


class Deck():
    def __init__(self) -> None:
        pass

    def deal(self) -> Card:
        pass

    def shuffle(self) -> None:
        pass

    @property
    def cards(self) -> set[Card]:
        pass


class Player():
    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        pass

    @property
    def cards(self) -> set[Card]:
        pass

    @property
    def hand(self) -> int:
        pass

    @property
    def money(self) -> int:
        pass

    @money.setter
    def money(self, amount: int) -> None:
        '''Adds the specified amount to the player's balance.'''

        pass

    def bet(self, amount: int) -> int:
        '''Withdraws an amount from the players money to wager'''
        pass
