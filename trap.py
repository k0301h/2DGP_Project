import pico2d
from map_floor import *

class Arrow_Trap:
    index_x = 0
    index_y = 0

    attack_range = 0

    image = None

    def __init__(self):
        if Arrow_Trap.image == None:
            Arrow_Trap.image = pico2d.load_image('./Textures/journal_entry_traps.png')

    def Place(self):
        for x in range(map_size):
            pass

        if map_floor_array[self.index_y][self.index_x] == 40:
            for c in range(1, map_size - self.index_x):
                if 2 <= map_floor_array[self.index_y][self.index_x + c] <= 29:
                    break
                else:
                    self.attack_range += 1

    def attack_boundary(self, unit):
        if map_floor_array[self.index_y][self.index_x] == 40:
            for c in range(1, map_size - self.index_x):
                if 2 <=  map_floor_array[self.index_y][self.index_x + c] <= 29:
                    break
                else:   # 이동가능한 블럭일 경우
                    if self.index_y * 60 - 30 <= unit.y <= self.index_y * 60 + 30 :
                        self.attack_range += 60
        elif map_floor_array[self.index_y][self.index_x] == 41:
            pass
