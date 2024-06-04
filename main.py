from time import sleep
from classes import Deck, Player
from colorama import Fore, Back
from time import sleep

from wagerError import WagerError
from zeroBalanceError import ZeroBalanceError

# colors
WHITE: str = Fore.WHITE
MAGENTA: str = Fore.MAGENTA
CYAN: str = Fore.CYAN
GREEN: str = Fore.LIGHTGREEN_EX
RED: str = Fore.RED
RESET: str = Fore.RESET
GOLD: str = Fore.YELLOW

# default chip winnings
PLAYER_NATURAL: float = 3.5
PLAYER_DEFAULT: float = 2
STAND_OFF: float = 1.5
STAND_OFF_BONUS: int = 50
DEALER_BUST: float = 1.5

# dealer stand hit targets
DEALER_HAND_TARGET = 15


def main() -> None:
    greeting()
    game()
    ...


def greeting() -> None:
    print(f'{MAGENTA}===============================================')
    print(f'{CYAN}-----------------Black Jack--------------------')
    print(f'{MAGENTA}===============================================')
    ...


def getName() -> str:
    valid: bool = False

    while not valid:
        name: str = input(f'{CYAN}Please enter your name\n')
        result: str = ''
        while not (result in ['y', 'n', 'yes', 'no']):
            result = input(f'Is [{name}] correct?\n(y/n):\t').lower()

        # check if indeed valid name
        valid = result in ['y', 'yes']
    return name


def game() -> None:
    # create deck and players
    deck: Deck = Deck()
    dealer: Player = Player(name='Dealer')
    player: Player = Player(name=getName())

    dealer.all_cards_visible = False
    player.all_cards_visible = True

    playing: bool = True

    while playing:
        print(f'{GREEN}------------------------------------------')
        print(f'Player: {player.name}\'s chips:\t$ {player.money}')
        print(f'{GREEN}------------------------------------------')

        # play round
        # TODO: handle ZeroBalanceError
        try:
            round(deck, player, dealer)
            player.clear_cards()
            dealer.clear_cards()
        except ZeroBalanceError as z:
            print(f'{RED}{z}')
            break

    ...


def round(deck: Deck, player: Player, dealer: Player) -> bool:
    '''Plays 1 round of Black Jack. \nReturns:\nTrue:   player won\nFalse:   dealer won OR standoff'''

    wager: int = getWager(player)
    if wager < 0:
        raise ZeroBalanceError(
            'We don\'t serve broke peasants! Be gone with you!')

    # the deck is empty:
    if deck.isEmpty():
        print(f'{RED}OOPS! The deck is empty. Start a new game...')
        return False

    # show deck
    print(f'{CYAN}{deck}')
    dealCards(deck, player, dealer)

    # check for naturals
    natural: int = getNatural(player, dealer)
    if natural == -1:
        player.money = int(wager * PLAYER_NATURAL)
        return True
    elif natural == 0:
        player.money = int(wager * STAND_OFF) + STAND_OFF_BONUS
        return False
    elif natural == 1:
        return False

    round_over: bool = False
    while not round_over:
        # no-one has a natural
        print(f'{MAGENTA}{dealer}')
        print(f'{GREEN}{player}')

        if not stand():
            # hit
            player.cards = deck.deal()  # type: ignore
        else:
            round_over = True

        sleep(1)

        # check if bust
        if player.bust:
            # dealer auto wins
            print(f'{GOLD}-----------------------------------------------------')
            print(f'{CYAN}OOPS! You have a bust. Dealer wins by default...')
            print(f'{GOLD}-----------------------------------------------------')
            print(f'{MAGENTA}You are no match for me...')
            print(f'{dealer}')
            print(f'{GREEN}{player}')
            return False

    # now dealer plays after player
    print(f'{MAGENTA}Dealer is playing...')
    sleep(1)
    stand_dealer(deck, dealer)

    # check if dealer bust
    if dealer.bust:
        print(f'{GOLD}-----------------------------------------------------')
        print(f'{CYAN}Dealer went bust. Player wins by default...')
        print(f'{MAGENTA}You won\'t be so lucky next time, {player.name}')
        print(f'{GOLD}-----------------------------------------------------')
        player.money = int(wager * DEALER_BUST)
        print(f'{MAGENTA}{dealer}')
        print(f'{GREEN}{player}')
        print(f'''{GOLD} Player won {GREEN} $ {
              int(wager*0.5)}{GOLD} in earings!''')
        return True

    # : compare hands
    compare_hands(player, dealer, wager)
    return True


def compare_hands(player: Player, dealer: Player, wager: int) -> None:
    '''Compares the hands of both players.'''
    if player.hand == dealer.hand:
        # standoff
        print(f'{GOLD}-----------------------------------------------------')
        print(f'{CYAN}\nIts a DRAW!')
        print(f'{GOLD}{player.name} receives {GREEN}$ 50.00')
        print(f'{GOLD}-----------------------------------------------------')
        player.money = wager + STAND_OFF_BONUS
    elif player.hand > dealer.hand:
        # player wins
        print(f'{GOLD}-----------------------------------------------------')
        print(f'{CYAN}\n{player.name} won.')
        print(f'{MAGENTA}I\'ll have you next time...')
        print(f'{GOLD}-----------------------------------------------------')
        player.money = int(wager*PLAYER_DEFAULT)
    else:
        # dealer wins
        print(f'{GOLD}-----------------------------------------------------')
        print(f'{CYAN}\nDealer won.')
        print(f'{MAGENTA}A failed apprentice makes for a foolish master.')
        print(f'{GOLD}-----------------------------------------------------')

    print(f'{MAGENTA}{dealer}')
    print(f'{GREEN}{player}')
    return None


def stand_dealer(deck: Deck, dealer: Player) -> None:
    done: bool = False
    while not done:
        if dealer.hand <= DEALER_HAND_TARGET:
            # hit
            print(f'{MAGENTA}Dealer is hitting...')
            sleep(.5)
            dealer.cards = deck.deal()  # type: ignore
        else:
            # stand
            print(f'{MAGENTA}Dealer stands...')
            sleep(.5)
            dealer.all_cards_visible = True
            break


def stand() -> bool:
    valid: bool = False
    result: str = input(
        f'{CYAN}Do you want to hit or stand?\nOptions: [ hit, h, stand, s ]\n')

    while not valid:
        if result.lower() in ['hit', 'stand', 'h', 's']:
            valid = True
            break
        print(f'''{RED}Input [{result}] is not an option. Options: {CYAN}[{MAGENTA} hit{
              CYAN},{MAGENTA} stand{CYAN}, {MAGENTA}h{CYAN}, {MAGENTA}s{CYAN}]''')
        result = input(f'{CYAN}Do you want to hit or stand?')

    # valid result
    return result.lower() in ['stand', 's']


def getNatural(player: Player, dealer: Player) -> int:
    '''Returns order of natural:
    -1 : \t Player has natural
    0  : \t Both have natural
    1  : \t Dealer has natural
    2  : \t Neither have a natural
    '''
    if player.has_natural and dealer.has_natural:
        print(f'{GOLD}-----------------------------------------------------')
        print(f'{CYAN}Its a DRAW!')
        print(f'{GOLD}Player receives {GREEN}$ 50.00')
        print(f'{GOLD}-----------------------------------------------------')
        return 0

    if dealer.has_natural:
        print(f'{GOLD}-----------------------------------------------------')
        print(f'{MAGENTA}My luck is unmatched!')
        print(f'{CYAN}Round over. Dealer won with a natural')
        print(f'{GOLD}-----------------------------------------------------')
        return 1

    if player.has_natural:
        print(f'{GOLD}-----------------------------------------------------')
        print(f'{GOLD}CONGRATS! You have a Natural!')
        print(f'{GOLD}-----------------------------------------------------')
        return -1

    return 2


def dealCards(deck: Deck, player: Player, dealer: Player) -> None:
    '''Deals cards to each player. If there are no more cards, returns False, else return True.'''
    print(f'{CYAN}-----------------------------------------------------')
    print(f'{CYAN}Dealing cards...')
    print(f'{CYAN}-----------------------------------------------------')
    sleep(1.5)
    dealer.all_cards_visible = False

    for _ in range(2):
        player.cards = deck.deal()  # type: ignore
        dealer.cards = deck.deal()  # type: ignore

    # !Deprecated: # display cards
    # print(f'{MAGENTA}{dealer}')
    # print(f'{GREEN}{player}')


def getWager(player: Player) -> int:
    valid: bool = False

    while not valid:
        result: str = input(f'{CYAN}How much do you want to wager?\n$ {GREEN}')
        try:
            amount: int = abs(int(result))
            player.bet(amount)
            valid = True
        except ValueError:
            print(f'{RED}[{result}] is not a valid integer!')
            valid = False
        except ZeroBalanceError as z:
            print(f'{RED}Not enough money - Away with you!')
            return -1
        except WagerError:
            print(f'''{RED}You do not have enough money.\n
                  Balance:\t $ {player.money}
                  Amount:\t $ {amount}
                  ''')
            valid = False
    print(f'{CYAN}{player.name} wagers {GREEN}$ {amount}')
    return amount


if __name__ == '__main__':
    main()
