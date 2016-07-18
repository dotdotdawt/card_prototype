import pygame

# Globals
LOW = False
HIGH = True
VID_QUALITY = LOW
TXT_QUALITY = HIGH
COST = 'cost'
ATK = 'atk'
HP = 'hp'
NAME = 'name'
BG = 'backdrop'
SELECTED = 'selected'
IN_PLAY = 'in_play'
DMG = 'dmg'
TARGET = 'target'
UNFILLED = 'unfilled'
FILLED = 'filled'
CARD_TXT_TYPES = [COST, ATK, HP, NAME]
MANA_TXT_TYPES = [UNFILLED, FILLED]


class Widget(object):
    '''
    Base class for pygame surfaces and subsequent child fields. For example,
    Card is a TextWidget created from Widget that displays data about a card.
    '''
    def __init__(self, settings, x=0, y=0, x_size=0, y_size=0, bg_color=None):
        '''
        cfg: Settings()
        x, y: int coords
        base: (x, y)
        base_size: size of surface width, height as (int, int)
        bg_color = (int, int, int)

        bg_img: pygame Surface
        bg_rect: bg_img.rect
        bg: (bg_img, bg_rect)


        Args:
            settings:
            x:
            y:
            x_size:
            y_size:
            bg_color:
        '''
        self.cfg = settings
        self.x = x
        self.y = y
        self.base = (x, y)
        self.base_size = (x_size, y_size)
        self.bg_img = pygame.surface.Surface(self.base_size)
        self.bg_rect = self.bg_img.get_rect()
        self.bg_color = bg_color

        # Force bg surface to have shade
        if not bg_color:
            self.bg_color = (100, 100, 200)

    def get_bg_color(self):
        '''
        Tool for getting the surface color depending on state.

        Returns:
            (int, int, int) or None
        '''
        return self.bg_color

    def update(self):
        '''Fills the background surface.'''
        self.base = (self.x, self.y)
        self.bg_rect.topleft = self.base
        self.bg_img.fill(self.get_bg_color())
        self.bg = (self.bg_img, self.bg_rect)

    def get_clicked(self, x, y):
        '''
        Returns True if input coordinates land on this Widget.

        Args:
            x: int
            y: int

        Returns:
            Boolean
        '''
        min_x = self.base[0]
        max_x = self.base[0] + self.base_size[0]
        min_y = self.base[1]
        max_y = self.base[1] + self.base_size[1]
        if x >= min_x and x <= max_x:
            if y >= min_y and y <= max_y:
                return True
        return False


class TextContainer(object):
    '''
    Base class for anything directly converted to text.
    '''
    def __init__(self, settings, txt_type=None, font_type=None, font_size=30):
        self.cfg = settings
        self.txt_type = txt_type
        self.text = ''
        self.font = pygame.font.SysFont(self.cfg.font_types[txt_type],
                                        self.cfg.sizes[txt_type])
        self.x = 0
        self.y = 0
        self.x_offset = 0
        self.y_offset = 0
        self.fg_color = (200, 200, 255)
        self.bg_color = None

        if txt_type in CARD_TXT_TYPES:
            self.x_offset = self.cfg.offsets[txt_type][0]
            self.y_offset = self.cfg.offsets[txt_type][1]
            self.fg_color = self.cfg.colors[txt_type][0]
            self.bg_color = self.cfg.colors[txt_type][1]
        elif txt_type in MANA_TXT_TYPES:
            self.fg_color = self.cfg.colors[txt_type][0]
            self.bg_color = self.cfg.colors[txt_type][1]

    def update_text(self, text, format=True):
        '''
        Updates pygame font object with input text.

        Args:
            text: str, int, list -- anything that can be converted to str
        '''
        if format:
            self.text = ' %s ' % str(text)
        else:
            self.text = text
        self.render_text()

    def render_text(self):
        '''
        Creates the pygame object set to display.
        '''
        if self.bg_color:
            self.img = self.font.render(self.text, True, self.fg_color, self.bg_color)
        else:
            self.img = self.font.render(self.text, True, self.fg_color)

        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x, self.y)

    def remap_with_parent(self, parent):
        '''
        Remaps this object using a specified parent.

        Args:
            parent: Widget, TextWidget, Card, etc.
        '''
        self.x = parent.x + self.x_offset
        self.y = parent.y + self.y_offset


class TextWidget(Widget):
    '''
    txt: dict of TextContainer objects indexed by txt_type
    txt_types: list of strings containing types of text to use
        ex: ['cost', 'name', 'dmg', 'target']
    cfg: Settings()


    '''
    def __init__(self, settings, x=0, y=0, x_size=0, y_size=0, bg_color=None):
        super(TextWidget, self).__init__(settings, x=x, y=y, x_size=x_size,
                                         y_size=y_size, bg_color=bg_color)
        #self.cfg = settings
        self.txt = {}
        self.txt_types = []

    def setup_children(self):
        '''
        Must be called from child class.

        '''
        for txt_type in self.txt_types:
            self.create_txt_container(self.cfg, txt_type)

    def create_txt_container(self, settings, txt_type=None, font_type=None, font_size=30):
        self.txt[txt_type] = TextContainer(settings, txt_type, font_type, font_size)
        self.txt[txt_type].remap_with_parent(self)

    def get_child_displays(self):
        imgs = {}
        rects = {}

        for txt_type in self.txt_types:
            if txt_type == COST:
                self.txt[txt_type].update_text(self.cost)
            elif txt_type == ATK:
                self.txt[txt_type].update_text(self.atk)
            elif txt_type == HP:
                self.txt[txt_type].update_text(self.hp)
            elif txt_type == NAME:
                self.txt[txt_type].update_text(self.name)
            elif txt_type == DMG:
                self.txt[txt_type].update_text(self.dmg)
            elif txt_type == TARGET:
                self.txt[txt_type].update_text(self.target)
            elif txt_type == UNFILLED:
                txt = 'A' * self.unfilled
                self.txt[txt_type].update_text(txt, format=False)
            elif txt_type == FILLED:
                txt = 'B' * self.filled
                self.txt[txt_type].update_text(txt, format=False)
            else:
                self.txt[txt_type].update_text('Cannot find update')

            imgs[txt_type] = self.txt[txt_type].img
            rects[txt_type] = self.txt[txt_type].rect

        return imgs, rects

    def update(self):
        '''Fills the background surface, updates the render of txt.'''
        self.base = (self.x, self.y)
        self.bg_rect.topleft = self.base
        self.bg_img.fill(self.get_bg_color())
        self.bg = (self.bg_img, self.bg_rect)

        return self.get_child_displays()


class Creature(TextWidget):
    def __init__(self, settings, x=0, y=0, x_size=180, y_size=240,
                 bg_color=None, model=None):
        super(Creature, self).__init__(settings, x=x, y=y, x_size=x_size,
                                        y_size=y_size, bg_color=bg_color)
        self.model = model
        self.cost = model.cost
        self.hp = model.hp
        self.atk = model.atk
        self.name = model.name
        self.txt_types = [COST, ATK, HP, NAME]

        self.selected = False
        self.selectable = False
        self.played = False
        self.sleeping = True

        self.setup_children()

    def get_bg_color(self):
        '''
        Tool for getting the surface color depending on state.

        Returns:
            (int, int, int) or None
        '''
        if self.selectable:
            return self.cfg.colors['selectable'][0]
        elif self.selected:
            return self.cfg.colors['selected'][0]
        elif not self.selectable and self.played:
            return self.cfg.colors['played'][0]

        else:
            return self.cfg.colors['backdrop'][0]

    def update_txt_location(self):
        for txt_type in self.txt_types:
            self.txt[txt_type].remap_with_parent(self)

    def reset_to_hand(self):
        self.x = 5 + (186 * self.slot)
        self.y = 515
        self.update_txt_location()


class EndTurnButton(TextWidget):
    def __init__(self, settings, x=992, y=792, x_size=192, y_size=56,
                 bg_color=None):
        self.inactive = False
        self.ready = True
        self.exhausted = False
        super(EndTurnButton, self).__init__(settings, x=x, y=y, x_size=x_size,
                                       y_size=y_size, bg_color=bg_color)
        self.setup_children()

    def get_bg_color(self):
        '''
        Tool for getting the surface color depending on state.

        Returns:
            (int, int, int) or None
        '''
        color = (0, 0, 33)
        if self.inactive:
            color = (50, 50, 50)
        if self.ready and self.exhausted:
            color = (10, 200, 10)
        elif self.ready and not self.exhausted:
            color = (150, 150, 10)
        self.bg_img.fill(color)
        return color


class ManaBar(TextWidget):
    def __init__(self, settings, x=12, y=792, x_size=0, y_size=0,
                 bg_color=None):
        super(ManaBar, self).__init__(settings, x=x, y=y, x_size=x_size,
                                      y_size=y_size, bg_color=bg_color)
        self.txt_types = [UNFILLED, FILLED]
        self.filled = 0
        self.unfilled = 0
        self.setup_children()

    def update_player_mana(self, player):
        self.filled = player.mana
        self.unfilled = player.mana_max