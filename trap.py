import pico2d

class Arrow_Trap:
    X = 0
    Y = 0

    image = None

    def __init__(self):
        if Arrow_Trap.image == None:
            Arrow_Trap.image = pico2d.load_image('./Textures/journal_entry_traps.png')
