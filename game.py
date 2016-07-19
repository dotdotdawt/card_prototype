import pygame
import random
import collection
import widget


class Game(object):
    '''
    Handles pygame inputs, pygame clock, screen, catalog of existing
    cards, and anything else known to the user.

    Attributes:
        selection: card instance or None
        hand: list of card instances

    '''

    def __init__(self, cfg, x=1200, y=860):
        # basics
        self.running = True
        self.left = 1
        self.right = 3
        self.fps = 60
        self.cfg = cfg
        self.hands_given = False
        self.selection = None
        self.cards = []

        # minx, maxx, miny, maxy
        self.play_bounds = [0, x, 0, y / 2]
        self.resolution = (x, y)
        self.bg_color = (100, 190, 141)

    def setup(self):
        '''
        Basic pygame init.
        '''
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.resolution)
        self.fps_clock = pygame.time.Clock()

        # Decide who goes first, placement is decided on
        # Player() instantiation
        first = False
        if random.randint(1, 100) >= 50:
            first = True
        self.players = [collection.Player(self.cfg, first),
                        collection.Player(self.cfg, not first)]
        self.end_turn_button = widget.EndTurnButton(self.cfg)
        self.mana_bar = widget.ManaBar(self.cfg)

    def start(self):
        for _ in range(5):
            self.draw_card()

    def draw_card(self):
        '''
        Draws a card from deck.
        '''
        self.cards.append(self.players[0].draw_card())
        self.players[0].update_hand()

    def play_card(self, player, card, slot=0):
        '''
        Plays a card from hand.
        '''
        card.set_to_in_play_slot(slot)
        card.played = True
        card.selected = False
        self.selection = None

        print 'playing %s' % card.name
        player.hand.remove(card)
        player.played_cards.append(card)
        player.mana -= card.cost

        self.mana_bar.update_player_mana(player)
        self.players[0].update_hand()

    def finish_turn(self):
        '''
        finish_turn should likely be exclusive to the person playing.
        We need to make something that involves receiving external data
        in order to process the other turn ending into us.
        '''
        self.end_turn_button.ready = False
        self.end_turn_button.inactive = True

    def start_turn(self):
        '''
        Data received.
        '''
        if not self.hands_given:
            self.start()
            self.hands_given = True
        self.end_turn_button.ready = True
        self.end_turn_button.inactive = False
        self.draw_card()
        player = self.players[0]
        player.mana_max += 1
        player.mana = player.mana_max
        self.mana_bar.update_player_mana(player)

    def update(self):
        '''
        Shows everything on the screen in order.
        '''
        # Wipe
        self.refresh_screen()

        # End Turn Button
        self.end_turn_button.update()
        self.screen.blit(self.end_turn_button.bg[0],
                         self.end_turn_button.bg[1])

        # Mana Bar
        mana = self.players[0].mana
        self.mana_bar.update_player_mana(self.players[0])
        imgs, rects = self.mana_bar.update()
        for name in imgs:
            self.screen.blit(imgs[name], rects[name])

        # Cards
        for card in self.cards:
            # force selected card to cursor
            if card.selected:
                card.x, card.y = pygame.mouse.get_pos()

            # In play
            if card.played:
                if card.sleeping:
                    card.selectable = False
                else:
                    card.selectable = True

            # In hand
            else:
                player = self.players[0]
                if player.mana >= card.cost:
                    card.selectable = True
                else:
                    card.selectable = False

            # displays a card in full
            imgs, rects = card.update()
            self.screen.blit(card.bg[0], card.bg[1])
            for name in imgs:
                self.screen.blit(imgs[name], rects[name])

        pygame.display.flip()

    def refresh_screen(self):
        '''
        Just wipes the screen.
        '''
        self.screen.fill(self.bg_color)

    def main_loop(self):
        '''
        Handles events, then runs updates at FPS intervals.
        '''
        while self.running:
            for event in pygame.event.get():

                #### Keyboard ####
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_q:
                        pass

                #### Mouse ####
                if event.type == pygame.MOUSEBUTTONUP:

                    ## Left click
                    if event.button == self.left:
                        x, y = pygame.mouse.get_pos()

                        if self.selection:
                            print self.selection
                            min_x = [(i*164)-25 for i in range(6)]
                            min_y = 460 - 25
                            max_x = [i+120 for i in min_x]
                            max_y = min_y + 160
                            slot = 0
                            found = False
                            for i in range(len(min_x)):
                                if y >= min_y and y <= max_y:
                                        if x >= min_x[i] and x <= max_x[i]:
                                            player = self.players[0]
                                            card = self.selection
                                            if not found:
                                                print i
                                                self.play_card(player, card, i)
                                                found = True

                        # User free to select something
                        else:
                            ## End turn button
                            if self.end_turn_button.get_clicked(x, y):
                                if self.end_turn_button.ready:
                                    self.finish_turn()
                                else:
                                    self.start_turn()
                            ## Hand cards
                            for cards in self.players[0].hand, self.players[1].hand:
                                for card in cards:
                                    card.selected = False
                                    if card.get_clicked(x, y):
                                        if card.selectable:
                                            self.selection = card
                                            card.selected = True
                            ## Cards in play
                            for card in self.players[0].played_cards:
                                card.selected = False
                                if card.get_clicked(x, y):
                                    if card.selectable:
                                        self.selection = card
                                        card.selected = True

                    ## Right click
                    elif event.button == self.right:
                        self.selection = None

            # Normal actions
            self.update()
            self.fps_clock.tick(self.fps)

        pygame.quit()