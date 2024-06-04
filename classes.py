from random import shuffle as RandomShuffle
from wagerError import WagerError
from zeroBalanceError import ZeroBalanceError


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

    def __str__(self) -> str:
        return f'{self.name}'


class Ace(Card):
    def __init__(self, name: str, value: int) -> None:
        super().__init__(name, 10)

    def min_value(self) -> int:
        '''Sets and returns value to 1.'''
        self._value = 1
        return self._value

    def max_value(self) -> int:
        '''Sets and returns value to 10.'''
        self._value = 10
        return self._value


class Deck():
    def __init__(self) -> None:
        ranks: dict = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                       '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10}
        suites: set = {'Hearts', 'Diamonds', 'Clubs', 'Spades'}
        deck: set[tuple[str, int]] = {
            (f'{rank} of {suite}', value) for rank, value in ranks.items() for suite in suites}

        self._cards: list[Card] = [
            Ace(card, value) if 'Ace' in card
            else Card(card, value)
            for card, value in deck]
        # shuffle deck after creation
        self.shuffle()

    def isEmpty(self) -> bool:
        return len(self._cards) == 0

    def deal(self) -> Card:
        return self.cards.pop()

    def shuffle(self) -> None:
        RandomShuffle(self._cards)

    @property
    def cards(self) -> list[Card]:
        return self._cards

    @cards.setter
    def cards(self, cards: set[Card]) -> None:
        self._cards = list(cards)

    def __str__(self) -> str:
        return f'{len(self.cards)} cards left in set.'


class Player():
    def __init__(self, name: str, money: int = 200) -> None:
        self._name: str = name
        self._money: int = money
        self._cards: set[Card] = set()
        self._hand: int = 0
        self._all_cards_visible: bool = True

    @property
    def has_natural(self) -> bool:
        return self._hand == 21

    @property
    def bust(self) -> bool:
        if self.hand <= 21:
            return False

        # bust
        # check if ace
        for card in self.cards:
            # if we have an un-minimized Ace -> minimize
            if 'Ace' in self.cards and card.value != 1:
                ace: Ace = Ace(card.name, card.value)
                ace.min_value
                self.cards.remove(card)
                self.cards.add(ace)
                break

        return self.hand > 21

    @property
    def all_cards_visible(self) -> bool:
        return self._all_cards_visible

    @all_cards_visible.setter
    def all_cards_visible(self, visibility: bool) -> None:
        self._all_cards_visible = visibility

    @property
    def name(self) -> str:
        return self._name

    @property
    def cards(self) -> set[Card]:
        return self._cards

    @cards.setter
    def cards(self, card: Card) -> None:
        if card is None:
            self._cards = set()
            self._hand = 0
        else:
            self._cards.add(card)
            self._hand += card.value

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

    def clear_cards(self) -> None:
        '''Clears the players cards and hand value.'''
        self._cards = set()
        self._hand = 0

    def bet(self, amount: int) -> int:
        '''Withdraws an amount from the player's money to wager'''
        amount = abs(amount)
        if self._money <= 0:
            raise ZeroBalanceError(f'{Player.name} is broke!')
        if self._money < amount:
            raise WagerError(
                f'{Player.name} does not have enough money!\n Balance: ${Player.money}')

        # money > amount
        self._money -= amount
        return amount

    def __str__(self) -> str:
        string: str = f'\n{self.name}'
        if self.all_cards_visible:
            string += f'\n[{", ".join(str(card) for card in self.cards)}]'
            string += f'\nHand value: {self.hand}\n'
        else:
            cards: list = list(self.cards)
            string += f'\n[{cards[0]}, {", ".join('?' for _ in cards[1:])}]'
        return string
