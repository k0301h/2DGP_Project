import pico2d
from map_floor import *

class Arrow_Trap:
    index_x = 0
    index_y = 0

    attack_range = 0
    attack_state = False

    image = None

    def __init__(self):
        if Arrow_Trap.image == None:
            Arrow_Trap.image = pico2d.load_image('./Textures/journal_entry_traps.png')

    def Place(self, number):
        for x in range(map_size):
            for y in range(map_size):
                if map_floor_array[y][x] == number + 40:
                    self.index_x, self.index_y = x , y
                    break
            if self.index_y and self.index_x:
                break

        if map_floor_array[self.index_y][self.index_x] == 40:
            for c in range(1, map_size - self.index_x):
                if 2 <= map_floor_array[self.index_y][self.index_x + c] <= 29:
                    break
                else:
                    self.attack_range += 1
        elif map_floor_array[self.index_y][self.index_x] == 41:
            for c in range(1, self.index_x):
                if 2 <= map_floor_array[self.index_y][self.index_x - c] <= 29:
                    break
                else:
                    self.attack_range += 1

    def Attack_boundary(self, unit):
        if map_floor_array[self.index_y][self.index_x] == 40 and not self.attack_state:
            if HEIGHT - self.index_y * 60 - 40 <= unit.Y <= HEIGHT - self.index_y * 60 + 40 and \
                    self.index_x * 60 + 30 <= unit.X <= self.index_x * 60 + 30 + self.attack_range * 60:
                unit.HP -= 2
                self.attack_state = True
                self.attack_state = True
        elif map_floor_array[self.index_y][self.index_x] == 41 and not self.attack_state:
            if HEIGHT - self.index_y * 60 - 40 <= unit.Y <= HEIGHT - self.index_y * 60 + 40 and \
                    self.index_x * 60 - 30 - self.attack_range * 60 <= unit.X <= self.index_x * 60 - 30:
                unit.HP -= 2
                self.attack_state = True
                self.Attack()

    def Attack(self):
        pass