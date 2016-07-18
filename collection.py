# Imports
import random
import widget

# Globals
LOW = False
HIGH = True
VID_QUALITY = LOW
TXT_QUALITY = HIGH
COST = 'cost'
ATK = 'atk'
HP = 'hp'
NAME = 'name'

# Helper functions
def get_deck_from_cards(cards):
    '''Get a deck from a collection of cards'''
    deck = []
    copies = 3
    for card in cards:
        for _ in range(copies):
            deck.append(cards[card])
    random.shuffle(deck)
    return deck

def draw_card_from_deck(deck):
    '''Returns: reference to template of a card to be instantiated'''
    return deck.pop(-1)

def get_default_collection():
    '''Returns dictionary containing default collection.'''
    all_cards = {}
    cards = []

    # Creatures
    cards.append(Creature(4, 'Heroic Loudmouth', None, 4, 5))
    cards.append(Creature(2, 'Corrupt Pipsqueak', None, 3, 2))
    cards.append(Creature(2, 'God of Value', None, 2, 2)) # Draw
    cards.append(Creature(6, 'Purple Elemental', None, 5, 7))

    # Spells
    #cards.append(Spell(2, 'Sleepbolt', ability='sleep', dmg=2, target='single'))

    for card in cards:
        all_cards[card.name] = card

    return all_cards


class Player(object):
    '''
    mana: int
    mana_max: int
    first: boolean
    second: boolean
    local: boolean -- causes change to logic
    '''

    def __init__(self, settings, first=False):
        self.mana_max = 0
        self.mana = 0
        self.cfg = settings
        self.first = first
        self.second = not first
        self.max_hand_size = 6
        self.hand = []
        self.played_cards = []
        self.selection = None
        self.setup()

    def setup(self):
        self.collection = get_default_collection()
        self.deck = get_deck_from_cards(self.collection)

    def draw_card(self):
        slot = len(self.hand)
        new_card = draw_card_from_deck(self.deck)

        # Deal with type and create instance
        if new_card.type == 'Creature':
            card_model = Creature(new_card.cost, new_card.name, new_card.ability,
                                  new_card.atk, new_card.hp)
            card_instance = widget.Creature(self.cfg, model=card_model)

        elif new_card.type == 'Spell':
            card_instance = Spell(new_card.cost, new_card.name, new_card.ability,
                                  new_card.dmg, new_card.target)

        # If it can fit
        if slot >= self.max_hand_size:
            card_instance.discarded = True
            #self.discard(card_instance)
        else:
            self.hand.append(card_instance)

        return card_instance

    def update_hand(self):
        for i in range(len(self.hand)):
            self.hand[i].slot = i
            self.hand[i].reset_to_hand()

# Card > Creature, Spell
class Card(object):
    '''
    cost: int
    name: str
    type: str
    ability: Not Implemented
    '''
    type = 'Card'

    def __init__(self, cost=0, name=None, ability=None):
        self.cost = 0
        self.name = ''
        self.ability = None
        if cost:
            self.cost = cost
        if name:
            self.name = name
        if ability:
            self.ability = ability

class Creature(Card):
    '''
    atk: int
    hp: int
    '''

    def __init__(self, cost=0, name=None, ability=None, atk=0, hp=0):
        self.type = 'Creature'
        self.atk = atk
        self.hp = hp

        super(Creature, self).__init__(cost=cost, name=name, ability=ability)

class Spell(Card):
    '''
    dmg: int
    target: Not Implemented
    '''

    def __init__(self, cost=0, name=None, ability=None, dmg=0, target=None):
        self.type = 'Spell'
        self.dmg = dmg
        self.target = target

        super(Spell, self).__init__(cost=cost, name=name, ability=ability)