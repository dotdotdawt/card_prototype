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

        # Decide who goes first
        first = random.randint(0, 1)
        print 'Going first? %s' % first

        self.playing = collection.Player(self.cfg, first)
        self.waiting = collection.Player(self.cfg, not first)
        self.players = [self.playing, self.waiting]
        if first:
            self.playing.mana_bar = widget.ManaBar(self.cfg)
            self.waiting.mana_bar = widget.ManaBar(self.cfg, enemy=True)
        else:
            self.playing.mana_bar = widget.ManaBar(self.cfg, enemy=True)
            self.waiting.mana_bar = widget.ManaBar(self.cfg)

        self.mana_bars = [self.playing.mana_bar, self.waiting.mana_bar]
        x1, y1, x2, y2 = (self.mana_bars[0].x,
                          self.mana_bars[0].y,
                          self.mana_bars[1].x,
                          self.mana_bars[1].y)
        print '%i, %i, %i, %i' % (x1, y1, x2, y2)
        self.end_turn_button = widget.EndTurnButton(self.cfg)

        # Creature slots
        self.creature_slots = []
        x_offset = 25
        y_offset = 272
        x_size = 120
        y_size = 160
        new_slot = 0
        for xval in [(i * x_size) for i in range(6)]:
            for yval in [y_offset, y_offset + y_size]:
                self.creature_slots.append(widget.CreatureSlot(self.cfg,
                                                               x=xval+x_offset,
                                                               y=yval,
                                                               slot=new_slot))
                print new_slot
            new_slot += 1

    def start(self):
        self.hands_given = True
        self.draw_card(playing=False)
        for _ in range(5):
            self.draw_card(playing=True)
            self.draw_card(playing=False)

    def draw_card(self, playing=False):
        '''
        Draws a card from deck.
        playing means "target of card draw is playing player"
        '''
        if playing:
            player = self.playing
        else:
            player = self.waiting
        self.cards.append(player.draw_card())
        player.update_hand()

    def play_card(self, player, card, slot, y_offset):
        '''
        Plays a card from hand.
        '''
        card.set_in_play(slot, y_offset)
        self.selection = None
        print 'playing %s' % card.name
        player.hand.remove(card)
        player.played.append(card)
        player.mana -= card.cost
        player.mana_bar.update_mana(player)
        player.update_hand()

    def change_ownership(self):
        p1, p2 = self.waiting, self.playing
        self.playing, self.waiting = p1, p2

    def finish_turn(self):
        '''
        finish_turn should likely be exclusive to the person playing.
        We need to make something that involves receiving external data
        in order to process the other turn ending into us.
        '''
        if not self.hands_given:
            self.start()

        self.change_ownership()
        self.end_turn_button.reset(True)

        self.playing.mana_max += 1
        self.playing.mana = self.playing.mana_max
        self.draw_card(playing=True)
        for card in self.cards:
            if card in self.playing.played:
                card.wake()

    def start_turn(self):
        '''
        Data received.
        '''
        if not self.hands_given:
            self.start()

        self.change_ownership()
        self.end_turn_button.reset(True)

        self.playing.mana_max += 1
        self.playing.mana = self.playing.mana_max
        self.draw_card(playing=True)

    def update(self):
        '''
        Shows everything on the screen in order.
        '''
        # Wipe
        self.refresh_screen()

        # End Turn Button
        self.end_turn_button.update()
        self.screen.blit(self.end_turn_button.bg[0], self.end_turn_button.bg[1])

        # Mana Bar
        for mana_bar in [self.playing.mana_bar, self.waiting.mana_bar]:
            imgs, rects = mana_bar.update()
            for name in imgs:
                self.screen.blit(imgs[name], rects[name])

        for c_slot in self.creature_slots:
            c_slot.update()
            self.screen.blit(c_slot.bg[0], c_slot.bg[1])

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
                if self.playing.mana >= card.cost:
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
                if event.type == pygame.MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()
                    for c_slot in self.creature_slots:
                        c_slot.set_hover(x, y)

                #### Keyboard ####
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_q:
                        print self.playing.mana
                        print self.waiting.mana

                #### Mouse ####
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    print x, y

                    ## Left click
                    if event.button == self.left:
                        if self.selection:
                            if isinstance(self.selection, widget.Creature):
                                #print self.selection

                                found = False
                                for c_slot in self.creature_slots:
                                    c_slot.set_hover(x, y)
                                    if c_slot.hover and c_slot.empty:
                                        y_slot = c_slot
                                        print 'nugget %i ' % c_slot.slot
                                        if not found:
                                            #if c_slot
                                            c_slot.occupy(self.selection)
                                            self.play_card(self.playing,
                                                           self.selection,
                                                           c_slot.slot,
                                                           c_slot.y)
                                            found = True
                                    if c_slot.hover and not c_slot.empty:
                                        c_slot.card.combat(self.selection)

                        # User free to select something
                        else:
                            ## End turn button
                            if self.end_turn_button.get_clicked(x, y):
                                #if self.end_turn_button.ready:
                                self.finish_turn()
                                #else:
                                #    self.start_turn()
                            ## Hand cards
                            for cards in self.playing.hand, self.waiting.hand:
                                for card in cards:
                                    card.selected = False
                                    if card.get_clicked(x, y):
                                        if card.selectable:
                                            self.selection = card
                                            card.selected = True
                            ## Cards in play
                            for card in self.playing.played:
                                card.selected = False
                                if card.get_clicked(x, y):
                                    if card.selectable:
                                        self.selection = card
                                        card.selected = True

                    ## Right click
                    elif event.button == self.right:
                        self.selection = None
                        for card in self.cards:
                            card.selected = False

            # Normal actions
            self.update()
            self.fps_clock.tick(self.fps)

        pygame.quit()