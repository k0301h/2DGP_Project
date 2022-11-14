import pico2d
import game_framework
from map_floor import *

PIXEL_PER_METER = (10 / 0.5)

RUN_SPEED_KMPH = 50.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Arrow_Trap:
    index_x = 0
    index_y = 0
    
    arrow_X = 0
    arrow_Y = 0

    arrow_move_distance = 0

    attack_range = 0
    attack_state = False

    image = None
    attack_image = None

    def __init__(self):
        if Arrow_Trap.image == None:
            Arrow_Trap.image = pico2d.load_image('./Textures/journal_entry_traps.png')
        if Arrow_Trap.attack_image == None:
            Arrow_Trap.attack_image = pico2d.load_image('./Textures/items.png')

    def Place(self, number):
        for x in range(map_size):
            for y in range(map_size):
                if map_floor_array[y][x] == number + 40:
                    self.index_x, self.index_y = x , y
                    self.arrow_x, self.arrow_y = x * 60, y * 60
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
        elif map_floor_array[self.index_y][self.index_x] == 41 and not self.attack_state:
            if HEIGHT - self.index_y * 60 - 40 <= unit.Y <= HEIGHT - self.index_y * 60 + 40 and \
                    self.index_x * 60 - 30 - self.attack_range * 60 <= unit.X <= self.index_x * 60 - 30:
                unit.HP -= 2
                self.attack_state = True

    def Attack_move(self):
        if map_floor_array[self.index_y][self.index_x] == 40:
            if self.arrow_move_distance <= self.attack_range * 60:
                run_move_speed = RUN_SPEED_PPS * game_framework.frame_time
                self.arrow_x += run_move_speed
                self.arrow_move_distance += run_move_speed
                print(self.arrow_x, self.arrow_y)
            else:
                self.attack_state = False
                self.arrow_y = self.index_y * 60
                self.arrow_x = self.index_x * 60

    def draw(self, character):
        print(self.arrow_x, self.arrow_y)
        self.attack_image.clip_draw(145, 2048 - 160, 95, 60, self.arrow_x - character.camera_move_x,
                                    self.arrow_y - character.camera_move_y, 60, 60)