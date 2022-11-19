from pico2d import *
from map_floor import *

class bullet:
    X = 0
    Y = 0
    direction = 0
    def __init__(self):
        if shotgun.image == None:
            shotgun.image = load_image('./Textures/items.png')

    def move(self):
        if self.direction == 0:
            if self.Conflict_check(1, 10):
                self.X += 10
        else:
            if self.Conflict_check(1, -10):
                self.X -= 10

    def Conflict_check(self, mode, move, unit = None):
        if mode == 1:     # X충돌 체크
            character_index_x = int((self.X + move) // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)
            for index_x in range(character_index_x - 2, character_index_x + 3):
                if 0 <= index_x < map_size\
                        (2 <= map_floor_array[character_index_y][index_x] <= 29 or 40 <= map_floor_array[character_index_y][index_x] <= 41) and \
                        abs(self.Y - (HEIGHT - character_index_y * 60)) < 58 and abs(self.X + move - index_x * 60) <= 55:
                    return False
        return True
    
    def draw(self, character):
        self.image.clip_draw(50, 2048 - 1865, 30, 30, character.X - character.camera_move_x - 17,
                                          character.Y - character.camera_move_y - 12, 20, 20)


class shotgun:
    ATK = 2
    Action = 0
    X = 0
    Y = 0
    image = None

    def __init__(self):
        if shotgun.image == None:
            shotgun.image = load_image('./Textures/items.png')

    def draw(self, character):
        if character.DIRECTION:
            self.image.clip_composite_draw(10, 2048 - 475, 120, 45, 0, 'h', character.X - character.camera_move_x - 17,
                                          character.Y - character.camera_move_y - 12, 40, 15)
        else:
            self.image.clip_composite_draw(10, 2048 - 475, 120, 45, 0, '', character.X - character.camera_move_x + 17,
                                          character.Y - character.camera_move_y - 12, 40, 15)