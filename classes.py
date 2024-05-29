from random import shuffle


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
        ranks: dict = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                       '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10}
        suites: set = {'Hearts', 'Diamonds', 'Clubs', 'Spades'}
        deck: set[tuple[str, int]] = {
            (f'{rank} of {suite}', value) for rank, value in ranks.items() for suite in suites}

        self._cards: list[Card] = [Card(card, value) for card, value in deck]

    def deal(self) -> Card:
        return self.cards.pop()

    def shuffle(self) -> None:
        shuffle(self._cards)

    @property
    def cards(self) -> list[Card]:
        return self._cards

    @cards.setter
    def cards(self, cards: set[Card]) -> None:
        self._cards = list(cards)


class Player():
    def __init__(self, name: str, money: int = 200) -> None:
        self._name: str = name
        self._money: int = money
        self._cards: set[Card] = set()
        self._hand: int = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def cards(self) -> set[Card]:
        return self._cards

    @property
    def hand(self) -> int:
        return self._hand

    @property
    def money(self) -> int:
        return self._money

    @money.setter
    def money(self, amount: int) -> None:
        '''Adds the specified amount to the player's balance.'''
        self._money += amount

    def bet(self, amount: int) -> int:
        '''Withdraws an amount from the player's money to wager'''
        amount = abs(amount)
        if self._money <= 0:
            return 0
        if self._money < amount:
            self._money = 0
            return self._money
        # money > amount
        self._money -= amount
        return amount
