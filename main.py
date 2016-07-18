import settings
import game

######
def main():
    cfg = settings.Settings()
    g = game.Game(cfg)
    g.setup()
    g.main_loop()

main()
