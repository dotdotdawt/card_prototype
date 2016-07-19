# Globals
COST = 'cost'
ATK = 'atk'
HP = 'hp'
NAME = 'name'
BG = 'backdrop'
SELECTED = 'selected'
SELECTABLE = 'selectable'
PLAYED = 'played'
DMG = 'dmg'
TARGET = 'target'
UNFILLED = 'unfilled'
FILLED = 'filled'

class Settings(object):
    '''
    Stores colors, offsets, backdrops and font types for text objects.
    '''
    def __init__(self):#bad       opusspecial
        #self.all_fonts = ['raavi', 'rod', 'microsoftyahei', 'simhei', 'browalliaupc', 'bodonipostercompressed', 'mingliupmingliumingliuhkscs', 'broadway', 'dilleniaupc', 'cambria', 'parchment', 'impact', 'calibri', 'arial', 'batangbatangchegungsuhgungsuhche', 'simplifiedarabicfixed', 'shonarbangla', 'wingdings3', 'extra', 'narkisim', 'segoeui', 'mistral', 'aparajitaitali', 'traditionalarabic', 'leelawadee', 'lucidacalligraphy', 'microsofthimalaya', 'cooperblack', 'opuschordssans', 'sakkalmajalla', 'berlinsansfb', 'consolas', 'microsoftuighur', 'georgia', 'frenchscript', 'wingdings', 'sylfaen', 'algerian', 'candara', 'aparajita', 'bauhaus93', 'oldenglishtext', 'verdana', 'gulimgulimchedotumdotumche', 'cordiaupc', 'bradleyhanditc', 'levenim', 'kodchiangupc', 'lucidafaxregular', 'palatinolinotype', 'opuschords', 'gabriola', 'lucidaconsole', 'lucidafax', 'tahoma', 'meiryomeiryomeiryouimeiryouiitalic', 'latha', 'opuschordssanscondensed', 'niagarasolid', 'segoeprint', 'opusjapanesechords', 'footlight', 'nyala', 'bernardcondensed', 'opusspecial', 'franklingothicmedium', 'laoui', 'microsofttaile', 'bookantiqua', 'pristina', 'lucidasans', 'opustext', 'garamond', 'corbel', 'segoeuisymbol', 'vrinda', 'constantia', 'jasmineupc', 'khmerui', 'miriam', 'kalinga', 'kartika', 'poorrichard', 'euphemia', 'arabictypesetting', 'opusromanchords', 'microsoftjhenghei', 'frankruehl', 'vinerhanditc', 'snapitc', 'malgungothic', 'centaur', 'freesiaupc', 'david', 'wingdings2', 'baskervilleoldface', 'segoescript', 'harrington', 'arialblack', 'daunpenh', 'gautami', 'vani', 'jokerman', 'monotypecorsiva', 'lucidabright', 'lucidahandwriting', 'mangal', 'albanyamt', 'msreferencesansserif', 'plantagenetcherokee', 'opusfunctionsymbols', 'angsanaupc', 'microsoftnewtailue', 'opusfiguredbassextras', 'browallianew', 'aharoni', 'stencil', 'britannic', 'mvboli', 'bookmanoldstyle', 'ebrima', 'msgothicmspgothicmsuigothic', 'trebuchetms', 'modernno20', 'opus', 'microsoftsansserif', 'gisha', 'utsaahitali', 'microsoftyibaiti', 'dfkaisb', 'comicsansms', 'simsunnsimsun', 'magneto', 'estrangeloedessa', 'juiceitc', 'opusnotenames', 'onyx', 'ravie', 'lilyupc', 'opuspercussion', 'couriernew', 'irisupc', 'dokchampa', 'freestylescript', 'msminchomspmincho', 'msreferencespecialty', 'andalus', 'playbill', 'cambriacambriamath', 'kunstlerscript', 'swtortrajan', 'showcardgothic', 'bell', 'vivaldi', 'cordianew', 'century', 'tunga', 'kristenitc', 'papyrus', 'moolboran', 'simsunextb', 'mongolianbaiti', 'opusspecialextra', 'informalroman', 'arialms', 'centurygothic', 'microsoftphagspa', 'hightowertext', 'vladimirscript', 'colonna', 'opusplainchords', 'berlinsansfbdemi', 'iskoolapota', 'opusmetronome', 'shruti', 'angsananew', 'kokilaitali', 'widelatin', 'opusornaments', 'meiryomeiryoboldmeiryouiboldmeiryouibolditalic', 'simplifiedarabic', 'vijaya', 'symbol', 'opusfiguredbass', 'swgamekeys', 'timesnewroman', 'bookshelfsymbol7', 'tempussansitc', 'maturascriptcapitals', 'segoeuisemibold', 'lucidablackletter', 'kaiti', 'utsaah', 'webdings', 'mingliuextbpmingliuextbmingliuhkscsextb', 'miriamfixed', 'californianfb', 'kokila', 'chiller', 'fangsong', 'harlowsolid', 'niagaraengraved', 'brushscript', 'eucrosiaupc']
        self.mana_bar_font = 'swgamekeys'
        self.card_font = 'oldenglishtext'
        self.valid_fonts = ['ebrima', 'corbel', 'oldenglishtext']
        self.txt_types = [COST, ATK, HP, NAME, DMG, TARGET, UNFILLED, FILLED]
        default = 'oldenglishtext'
        self.font_types = {COST: default,
                           ATK: default,
                           HP: default,
                           NAME:default,
                           DMG: default,
                           TARGET: default,
                           UNFILLED: self.mana_bar_font,
                           FILLED: self.mana_bar_font}
        self.sizes = {COST: 18,
                      ATK: 18,
                      HP: 18,
                      NAME: 14,
                      DMG: 26,
                      TARGET: 50,
                      UNFILLED: 42,
                      FILLED: 42}
        self.offsets = {COST: [5, 5],
                        ATK: [5, 126],
                        HP: [96, 126],
                        NAME: [4, 44]}
        self.colors = { COST: [(100, 255, 200), (200, 0, 200)],
                        ATK: [(100, 255, 200), None],
                        HP: [(100, 255, 200), None],
                        NAME: [(200, 200, 200), None],
                        BG: [(10, 10, 10), None],
                        PLAYED: [(180, 80, 140, 50), None],
                        SELECTED: [(10, 150, 10), None],
                        SELECTABLE: [(10, 100, 50), None],
                        UNFILLED: [(100, 100, 100), None],
                        FILLED: [(0, 180, 200, 30), None]}
        self.emotes = ['Heart of the cards is strong',
                       'Fuck you',
                       'Please no',
                       'Goddammit',
                       'Praise RNGESUS',
                       'WAKE UP',
                       'What the fuck was that',
                       'plz concede']