from pico2d import *
from map_floor import *
from math import sqrt
import game_framework

PIXEL_PER_METER = (10 / 0.5)

RUN_SPEED_KMPH = 150.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class bullet:
    X = 0
    Y = 0
    DIRECTION = 0
    save = 1
    run_speed = 0
    image = None
    def __init__(self):
        if bullet.image == None:
            bullet.image = load_image('./Textures/items.png')

    def Place(self, character, index):
        if character.DIRECTION:
            self.X = character.X - 10
        else:
            self.X = character.X + 60
        self.Y = character.Y - (index - 1) * 10
        self.save = 1
        self.DIRECTION = character.DIRECTION

    def move(self):
        self.run_speed = RUN_SPEED_PPS * game_framework.frame_time
        if self.DIRECTION == 0:
            if self.Conflict_check(1, self.run_speed):
                self.X += self.run_speed
            else:
                self.save = 0
        else:
            if self.Conflict_check(1, -self.run_speed):
                self.X -= self.run_speed
            else:
                self.save = 0

    def Conflict_check(self, mode, move, unit = None):
        if mode == 1:     # X충돌 체크
            character_index_x = int((self.X + move) // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)
            if not self.DIRECTION:
                character_index_x += 1
                if (2 <= map_floor_array[character_index_y][character_index_x] <= 29 or 40 <= map_floor_array[character_index_y][character_index_x] <= 41) and \
                        abs(self.Y - 10 - (HEIGHT - character_index_y * 60 - 30)) < 40 and abs(self.X + move - character_index_x * 60) <= 20:
                    return False
            else:
                for index_x in range(character_index_x - 1, character_index_x + 2):
                    if 0 <= index_x < map_size and \
                            (2 <= map_floor_array[character_index_y][index_x] <= 29 or 40 <= map_floor_array[character_index_y][index_x] <= 41) and \
                            abs(self.Y - 10 - (HEIGHT - character_index_y * 60 - 30)) < 40 and abs(self.X + move - index_x * 60 - 60) <= 0:
                        return False
        elif mode == 2:
            if sqrt((unit.X - self.X) ** 2 + (unit.Y - self.Y) ** 2) <= 40:
                unit.HP -= 1
                self.save = 0
        return True
    
    def draw(self, character):
        if self.save:
            self.image.clip_draw(50, 2048 - 1865, 30, 30, self.X - character.camera_move_x - 17,
                                              self.Y - character.camera_move_y - 12, 20, 20)


class shotgun:
    ATK = 2
    Action = 0
    X = 0
    Y = 0
    image = None
    bullet_object = [bullet() for _ in range(3)]

    timer = 0

    sound = None

    def __init__(self):
        if shotgun.image == None:
            shotgun.image = load_image('./Textures/items.png')
        self.sound = load_wav('./sound/shotgun_fire.wav')

    def update(self, character):
        self.timer += game_framework.frame_time
        if self.timer > 2:
            character.reload = True
            self.timer = 0

    def draw(self, character):
        if character.DIRECTION:
            self.image.clip_composite_draw(10, 2048 - 475, 120, 45, 0, 'h', character.X - character.camera_move_x - 17,
                                          character.Y - character.camera_move_y - 12, 40, 15)
        else:
            self.image.clip_composite_draw(10, 2048 - 475, 120, 45, 0, '', character.X - character.camera_move_x + 17,
                                          character.Y - character.camera_move_y - 12, 40, 15)