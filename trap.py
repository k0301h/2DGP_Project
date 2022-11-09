import pico2d
from map_floor import *

class Arrow_Trap:
    index_x = 0
    index_y = 0

    image = None

    def __init__(self):
        if Arrow_Trap.image == None:
            Arrow_Trap.image = pico2d.load_image('./Textures/journal_entry_traps.png')

    def attack_boundary(self):
        if map_floor_array[self.index_y][self.index_x] == 40:
            for c in range(3):
                if map_floor_array[self.index_y + c][self.index_x] == 0:
                    pass
                else:   # 이동가능한 블럭일 경우
                    pass
        elif map_floor_array[self.index_y][self.index_x] == 41:
            pass
